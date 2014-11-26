/*
    Argonne Leadership Computing Facility benchmark
    BlueGene/P version
    Messaging rate
    Written by Vitali Morozov <morozov@anl.gov>
    Updated 20090929: made bi-directional
*/
#include <mpi.h>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#ifdef HALO_BGQ
#include "q5d.h"
#endif

#define MAXN 150000     // repetition rate for a single pair test
#define MAXSKIP 20      // skip first tests to warm-up
#define N 10             // number of simumtaneous communications (available links)
#define NDIMS 5         // Cartesian mesh dimension
#define Hz 850.e6      // CPU clock rate, in Hz
#define DUPES 8        // Number of duplicate messages to send
#define LENGTH 1024    // message size, in doubles
#define L3CACHE 32     // last level cache in MB, used to flash the cache before each test

#define REQSPERDIM 4   // Max number of simultaneous requests per dimension

#ifdef HALO_TIMER_BGQ_TIMEBASE
typedef unsigned long long halo_time_t;

halo_time_t  timebase();

static halo_time_t timebase_diff(halo_time_t t1, halo_time_t t2) {
  return t2 - t1;
}

static double timebase_us(halo_time_t t) {
  return (double)( t ) / Hz * 1e6 ;
}

#define halo_timer(t1) *(t1) = timebase()
#define halo_time_ticks(t) (t)
#define halo_time_diff(t1, t2) timebase_diff((t1), (t2))
#define halo_time_us(td) timebase_us(td)
#endif

#ifdef HALO_TIMER_CLOCK_REALTIME
#include <time.h>
typedef struct timespec halo_time_t;

static halo_time_t timespec_diff(halo_time_t t1, halo_time_t t2) {
  halo_time_t res;
  res.tv_sec = t2.tv_sec - t1.tv_sec;
  if (t2.tv_nsec > t1.tv_nsec) {
    res.tv_nsec = t2.tv_nsec - t1.tv_nsec;
  } else {
    res.tv_sec--;
    res.tv_nsec = 1000000000L - t1.tv_nsec + t2.tv_nsec;
  }

  return res;
}

static double timespec_us(halo_time_t t) {
  return (t.tv_sec * 1e6 + ((double)t.tv_nsec) / 1e3);
}

#define halo_timer(t1) clock_gettime(CLOCK_REALTIME, t1)
#define halo_time_ticks(t) ((t).tv_nsec + ((long long)(t).tv_sec) * 1000000000)
#define halo_time_diff(t1, t2) timespec_diff((t1), (t2))
#define halo_time_us(td) timespec_us(td)

#endif


#ifdef FTN_UNDERSCORE
void durand_(double *seed, int *npts, double *x);
#define durand(seed, npts, x) durand_(seed, npts, x)
#else
void durand(double *seed, int *npts, double *x);
#endif

//TODO: Mainloop should be 50
int MAINLOOP = 10;  // 50 loops of 120ms = 60s 

int main( int argc, char *argv[] )
{
    int rc, d;
    int taskid, ntasks, i, j;
    int datalength = LENGTH;
    if (argc != 2){
      fprintf(stderr, "Missing arg for data length");
    }else{
      datalength = atoi(argv[1]);
      fprintf(stderr, "datalength set to %d", datalength);
    }

    int mainloopindex = 0;

    double sb[NDIMS][2][datalength];
    double rb[NDIMS][2][datalength];
    //double sb[NDIMS][2][datalength], rb[NDIMS][2][datalength]; // buffers: 2 displacements in each dimension

    halo_time_t t1, t2, tdelay;
    int dims[NDIMS], periods[NDIMS], reorder;
    MPI_Comm comm_cart;
    MPI_Request req[REQSPERDIM*NDIMS*DUPES];
    MPI_Status  stt[REQSPERDIM*NDIMS*DUPES];
    double seed, delay;
    int one;
    useconds_t udelay;
    int rank_src[2][NDIMS], rank_dst[2][NDIMS]; // For positive displacement and dimension 1, source rank is rank_src[0][1], destination rank is rank_dst[0][1];
                                                // For negative displacement and dimension 0, source rank is rank_src[1][0], destination rank is rank_dst[1][0];
    char *src, *trg; // memcpy buffers used to flash last level cache
    size_t LB;

    /*
    for ( i=0 ; i<NDIMS ; i++){
      sb[i][0] = malloc(sizeof(double)*datalength);
      sb[i][1] = malloc(sizeof(double)*datalength);
      rb[i][0] = malloc(sizeof(double)*datalength);
      rb[i][1] = malloc(sizeof(double)*datalength);
    }
    */

    LB = L3CACHE * 1024 * 1024;
    src = (char *)malloc( LB );
    trg = (char *)malloc( LB );

    rc = MPI_Init( &argc, &argv );
    assert(rc == MPI_SUCCESS);

    rc = MPI_Comm_rank( MPI_COMM_WORLD, &taskid );
    assert(rc == MPI_SUCCESS);

    rc = MPI_Comm_size( MPI_COMM_WORLD, &ntasks );
    assert(rc == MPI_SUCCESS);

#ifdef HALO_BGQ
    Q5D_Init();
    int32_t torus_coords[6];
    Q5D_Torus_coords(torus_coords);
    /* fprintf(stderr, "Rank %d torus coords: (%"PRId32", %"PRId32", %"PRId32", %"PRId32", %"PRId32", %"PRId32")", taskid,
              torus_coords[0], torus_coords[1], torus_coords[2],
              torus_coords[3], torus_coords[4], torus_coords[5]);
    */
    fprintf(stderr, "Rank %d torus coords: (%d, %d, %d, %d , %d, %d)\n", taskid,
              torus_coords[0], torus_coords[1], torus_coords[2],
              torus_coords[3], torus_coords[4], torus_coords[5]);

#endif

    for ( i = 0; i < NDIMS; i++ ) dims[i] = 0;
    rc = MPI_Dims_create( ntasks, NDIMS, dims );
    assert(rc == MPI_SUCCESS);

    if ( (NDIMS == 5) && (taskid == 0) ) printf( "Cartesian topology: %d x %d x %d x %d x %d\n", dims[0], dims[1], dims[2], dims[3], dims[4] );
    if ( (NDIMS == 3) && (taskid == 0) ) printf( "Cartesian topology: %d x %d x %d\n", dims[0], dims[1], dims[2] );

    //for ( i = 0; i < NDIMS; i++ ) periods[i] = 0; // no periods for this test
    
    // Setting periods = 1 for wrap-around
    for ( i = 0; i < NDIMS; i++ ) periods[i] = 1; // no periods for this test
    reorder = 1; // reorder is allowed
    rc = MPI_Cart_create( MPI_COMM_WORLD, NDIMS, dims, periods, reorder, &comm_cart);
    assert(rc == MPI_SUCCESS);

    // Generate disbalance and measure the longest delay
    seed = (double)taskid;
    one = 1;
    durand( &seed, &one, &delay );
    udelay = (useconds_t)(delay * 1e5 );

    rc = MPI_Barrier( comm_cart );
    assert(rc == MPI_SUCCESS);
    halo_timer(&t1);

    usleep( udelay );

    rc = MPI_Barrier( comm_cart );
    assert(rc == MPI_SUCCESS);
    halo_timer(&t2);
    /////////////////////////////////////////////////////

    tdelay = halo_time_diff(t1, t2);
    //fprintf( stderr, "Hello from rank %d of %d tasks: delay %ld microseconds\n", taskid, ntasks, udelay );
    if ( taskid == 0 ) fprintf( stderr, "Delay time: %lld pclks, %18.12lf microseconds\n",
        halo_time_ticks(tdelay), halo_time_us(tdelay) );


    for( i = 0; i < NDIMS; i++ )
    {
        rc = MPI_Cart_shift( comm_cart, i,  1, &rank_src[0][i], &rank_dst[0][i] );
        assert(rc == MPI_SUCCESS);
        rc = MPI_Cart_shift( comm_cart, i, -1, &rank_src[1][i], &rank_dst[1][i] );
        assert(rc == MPI_SUCCESS);

        int j;
        for ( j = 0; j < 2; j++ )
        {
          if ( taskid == 0 )
          {
            fprintf(stderr, "rank_src[%i][%i]=%i\n", j, i, rank_src[j][i]);
            fprintf(stderr, "rank_dst[%i][%i]=%i\n", j, i, rank_dst[j][i]);
          }
        }
    }
    fprintf(stderr, "rank_dst[%i][%i]=%i, setting sb to %d \n", j, i, rank_dst[j][i]);
    //i = memset(sb, taskid, NDIMS*2*datalength);
    
    // MAINOUTERLOOP
    for ( mainloopindex = 0 ; mainloopindex < MAINLOOP ; mainloopindex++ ){
      usleep(150000); // sleep for 150 ms 
    ///////////// Test Sendrecv without delay //////////////////
    memcpy( trg, src, LB );

    rc = MPI_Barrier( comm_cart );
    assert(rc == MPI_SUCCESS);
    halo_timer(&t1);

    for ( i = 0; i < NDIMS; i++ )
    {
        for ( d = 0; d < DUPES; d++ )
        {
          rc = MPI_Sendrecv( &sb[i][0][0], datalength, MPI_DOUBLE, rank_dst[0][i], 0, &rb[i][0][0], datalength, MPI_DOUBLE, rank_src[0][i], 0, comm_cart, MPI_STATUS_IGNORE );
          assert(rc == MPI_SUCCESS);
        }
        for ( d = 0; d < DUPES; d++ )
        {
          rc = MPI_Sendrecv( &sb[i][1][0], datalength, MPI_DOUBLE, rank_dst[1][i], 1, &rb[i][1][0], datalength, MPI_DOUBLE, rank_src[1][i], 1, comm_cart, MPI_STATUS_IGNORE );
          assert(rc == MPI_SUCCESS);
        }
    }

    rc = MPI_Barrier( comm_cart );
    assert(rc == MPI_SUCCESS);
    halo_timer(&t2);

    if( taskid == 0 ) fprintf( stderr, "Sendrecv no delay for %dx%d doubles: %lld pclks, %18.12lf microseconds\n",
        DUPES, datalength, halo_time_ticks(halo_time_diff(t1, t2)), halo_time_us(halo_time_diff(t1, t2)) );

    //////////// Test Sendrecv with delay ////////////////////
    memcpy( trg, src, LB );

    rc = MPI_Barrier( comm_cart );
    assert(rc == MPI_SUCCESS);
    halo_timer(&t1);

    usleep( udelay );

    for ( i = 0; i < NDIMS; i++ )
    {
        for ( d = 0; d < DUPES; d++ )
        {
            rc = MPI_Sendrecv( &sb[i][0][0], datalength, MPI_DOUBLE, rank_dst[0][i], 0, &rb[i][0][0], datalength, MPI_DOUBLE, rank_src[0][i], 0, comm_cart, MPI_STATUS_IGNORE );
            assert(rc == MPI_SUCCESS);
        }
        for ( d = 0; d < DUPES; d++ )
        {
            rc = MPI_Sendrecv( &sb[i][1][0], datalength, MPI_DOUBLE, rank_dst[1][i], 1, &rb[i][1][0], datalength, MPI_DOUBLE, rank_src[1][i], 1, comm_cart, MPI_STATUS_IGNORE );
            assert(rc == MPI_SUCCESS);
        }
    }

    rc = MPI_Barrier( comm_cart );
    assert(rc == MPI_SUCCESS);
    halo_timer(&t2);

    if( taskid == 0 ) fprintf( stderr, "Sendrecv wt delay time for %dx%d doubles: %lld pclks, %18.12lf microseconds\n",
        DUPES, datalength, halo_time_ticks(halo_time_diff(tdelay, halo_time_diff(t1, t2))), halo_time_us(halo_time_diff(tdelay, halo_time_diff(t1, t2)) ) );

    ///////////// Test ISend - Recv - Barrier without delay //////////////////
    memcpy( trg, src, LB );

    rc = MPI_Barrier( comm_cart );
    assert(rc == MPI_SUCCESS);
    halo_timer(&t1);

    for ( i = 0; i < NDIMS; i++ )
    {
        for ( j = 0; j < 2; j++ ) // displacement
        {
            for ( d = 0; d < DUPES; d++ )
            {
                rc = MPI_Isend( &sb[i][j][0], datalength, MPI_DOUBLE, rank_dst[j][i], 0, comm_cart, &req[0] );
                assert(rc == MPI_SUCCESS);
                rc = MPI_Recv ( &rb[i][j][0], datalength, MPI_DOUBLE, rank_src[j][i], 0, comm_cart, MPI_STATUS_IGNORE );
                assert(rc == MPI_SUCCESS);
            }
            rc = MPI_Barrier( comm_cart );
            assert(rc == MPI_SUCCESS);
        }
    }

    rc = MPI_Barrier( comm_cart );
    assert(rc == MPI_SUCCESS);
    halo_timer(&t2);

    if( taskid == 0 ) fprintf( stderr, "Isend-recv no delay for %dx%d doubles: %lld pclks, %18.12lf microseconds\n",
        DUPES, datalength, halo_time_ticks(halo_time_diff(t1, t2)), halo_time_us(halo_time_diff(t1, t2)) );

    ///////////// Test ISend - Recv - Barrier with delay //////////////////
    memcpy( trg, src, LB );

    rc = MPI_Barrier( comm_cart );
    assert(rc == MPI_SUCCESS);
    halo_timer(&t1);

    usleep( udelay );

    for ( i = 0; i < NDIMS; i++ )
    {
        for ( j = 0; j < 2; j++ ) // displacement
        {
            for ( d = 0; d < DUPES; d++ )
            {
                rc = MPI_Isend( &sb[i][j][0], datalength, MPI_DOUBLE, rank_dst[j][i], 0, comm_cart, &req[0] );
                assert(rc == MPI_SUCCESS);
                rc = MPI_Recv ( &rb[i][j][0], datalength, MPI_DOUBLE, rank_src[j][i], 0, comm_cart, MPI_STATUS_IGNORE );
                assert(rc == MPI_SUCCESS);
            }
            rc = MPI_Barrier( comm_cart );
            assert(rc == MPI_SUCCESS);
        }
    }

    rc = MPI_Barrier( comm_cart );
    assert(rc == MPI_SUCCESS);
    halo_timer(&t2);

    if( taskid == 0 ) fprintf( stderr, "Isend-recv wt delay for %dx%d doubles: %lld pclks, %18.12lf microseconds\n",
        DUPES, datalength, halo_time_ticks(halo_time_diff(tdelay, halo_time_diff(t1, t2))), halo_time_us(halo_time_diff(tdelay, halo_time_diff(t1, t2))));

    ///////////// Test ISend - Recv - Wait without delay //////////////////
    memcpy( trg, src, LB );

    rc = MPI_Barrier( comm_cart );
    assert(rc == MPI_SUCCESS);
    halo_timer(&t1);

    for ( i = 0; i < NDIMS; i++ )
    {
        for ( j = 0; j < 2; j++ ) // displacement
        {
            for ( d = 0; d < DUPES; d++ )
            {
                rc = MPI_Isend( &sb[i][j][0], datalength, MPI_DOUBLE, rank_dst[j][i], 0, comm_cart, &req[d * 2] );
                rc = MPI_Irecv( &rb[i][j][0], datalength, MPI_DOUBLE, rank_src[j][i], 0, comm_cart, &req[d * 2 + 1] );
            }
            rc = MPI_Waitall( 2 * DUPES, &req[0], &stt[0] );
            assert(rc == MPI_SUCCESS);
        }
    }

    rc = MPI_Barrier( comm_cart );
    assert(rc == MPI_SUCCESS);
    halo_timer(&t2);

    if( taskid == 0 ) fprintf( stderr, "Isend-Irecv no delay for %dx%d doubles: %lld pclks, %18.12lf microseconds\n",
        DUPES, datalength, halo_time_ticks(halo_time_diff(t1, t2)), halo_time_us(halo_time_diff(t1, t2)) );

    ///////////// Test ISend - Recv - Wait with delay //////////////////
    memcpy( trg, src, LB );

    rc = MPI_Barrier( comm_cart );
    assert(rc == MPI_SUCCESS);
    halo_timer(&t1);

    usleep( udelay );

    for ( i = 0; i < NDIMS; i++ )
    {
        for ( j = 0; j < 2; j++ ) // displacement
        {
            for ( d = 0; d < DUPES; d++ )
            {
                rc = MPI_Isend( &sb[i][j][0], datalength, MPI_DOUBLE, rank_dst[j][i], 0, comm_cart, &req[d * 2] );
                assert(rc == MPI_SUCCESS);
                rc = MPI_Irecv( &rb[i][j][0], datalength, MPI_DOUBLE, rank_src[j][i], 0, comm_cart, &req[d * 2 + 1] );
                assert(rc == MPI_SUCCESS);
            }
            rc = MPI_Waitall( 2 * DUPES, &req[0], &stt[0] );
            assert(rc == MPI_SUCCESS);
        }
    }

    rc = MPI_Barrier( comm_cart );
    assert(rc == MPI_SUCCESS);
    halo_timer(&t2);

    if( taskid == 0 ) fprintf( stderr, "Isend-Irecv wt delay for %dx%d doubles: %lld pclks, %18.12lf microseconds\n",
        DUPES, datalength, halo_time_ticks(halo_time_diff(tdelay, halo_time_diff(t1, t2))), halo_time_us(halo_time_diff(tdelay, halo_time_diff(t1, t2)) ));

    ///////////// Test ISend - Recv - Wait all 6 without delay //////////////////
    memcpy( trg, src, LB );

    rc = MPI_Barrier( comm_cart );
    assert(rc == MPI_SUCCESS);
    halo_timer(&t1);

    for ( i = 0; i < NDIMS; i++ )
    {
        for ( d = 0; d < DUPES; d++ )
        {
            rc = MPI_Isend( &sb[i][0][0], datalength, MPI_DOUBLE, rank_dst[0][i], 0, comm_cart, &req[4 * (i * DUPES + d)] );
            assert(rc == MPI_SUCCESS);
            rc = MPI_Irecv( &rb[i][0][0], datalength, MPI_DOUBLE, rank_src[0][i], 0, comm_cart, &req[4 * (i * DUPES + d) + 1] );
            assert(rc == MPI_SUCCESS);
        }

        for ( d = 0; d < DUPES; d++ )
        {
            rc = MPI_Isend( &sb[i][1][0], datalength, MPI_DOUBLE, rank_dst[1][i], 0, comm_cart, &req[4 * (i * DUPES + d) + 2] );
            assert(rc == MPI_SUCCESS);
            rc = MPI_Irecv( &rb[i][1][0], datalength, MPI_DOUBLE, rank_src[1][i], 0, comm_cart, &req[4 * (i * DUPES + d) + 3] );
            assert(rc == MPI_SUCCESS);
        }
    }

    rc = MPI_Waitall( 4 * NDIMS * DUPES, &req[0], &stt[0] );
    assert(rc == MPI_SUCCESS);

    rc = MPI_Barrier( comm_cart );
    assert(rc == MPI_SUCCESS);
    halo_timer(&t2);

    if( taskid == 0 ) fprintf( stderr, "12 at a time no delay for %dx%d doubles: %lld pclks, %18.12lf microseconds\n",
        DUPES, datalength, halo_time_ticks(halo_time_diff(t1, t2)), halo_time_us(halo_time_diff(t1, t2)) );

    ///////////// Test ISend - Recv - Wait all 6 with delay //////////////////
    memcpy( trg, src, LB );

    rc = MPI_Barrier( comm_cart );
    assert(rc == MPI_SUCCESS);
    halo_timer(&t1);

    usleep( udelay );

    for ( i = 0; i < NDIMS; i++ )
    {
        for ( d = 0; d < DUPES; d++ )
        {
            rc = MPI_Isend( &sb[i][0][0], datalength, MPI_DOUBLE, rank_dst[0][i], 0, comm_cart, &req[4 * (i * DUPES + d)] );
            assert(rc == MPI_SUCCESS);
            rc = MPI_Irecv( &rb[i][0][0], datalength, MPI_DOUBLE, rank_src[0][i], 0, comm_cart, &req[4 * (i * DUPES + d) + 1] );
            assert(rc == MPI_SUCCESS);
        }

        for ( d = 0; d < DUPES; d++ )
        {
            rc = MPI_Isend( &sb[i][1][0], datalength, MPI_DOUBLE, rank_dst[1][i], 0, comm_cart, &req[4 * (i * DUPES + d) + 2] );
            assert(rc == MPI_SUCCESS);
            rc = MPI_Irecv( &rb[i][1][0], datalength, MPI_DOUBLE, rank_src[1][i], 0, comm_cart, &req[4 * (i * DUPES + d) + 3] );
            assert(rc == MPI_SUCCESS);
        }
    }

    rc = MPI_Waitall( 4 * NDIMS* DUPES, &req[0], &stt[0] );
    assert(rc == MPI_SUCCESS);

    rc = MPI_Barrier( comm_cart );
    assert(rc == MPI_SUCCESS);
    halo_timer(&t2);

    if( taskid == 0 ) fprintf( stderr, "12 at a time wt delay for %dx%d doubles: %lld pclks, %18.12lf microseconds\n",
        DUPES, datalength, halo_time_ticks(halo_time_diff(tdelay, halo_time_diff(t1, t2))), halo_time_us(halo_time_diff(tdelay, halo_time_diff(t1, t2)) ) );
    } // MAINOUTERLOOP
    rc = MPI_Finalize();
    assert(rc == MPI_SUCCESS);

    free( src );
    free( trg );

    return 0;
}
