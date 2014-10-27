/* 
    Argonne Leadership Computing Facility benchmark
    BlueGene/P version
    Messaging rate 
    Written by Vitali Morozov <morozov@anl.gov>
    Updated 20090929: made bi-directional
*/    
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#include "q5d.h"

#define MAXN 150000     // repetition rate for a single pair test
#define MAXSKIP 20      // skip first tests to warm-up
#define N 6             // number of simumtaneous communications (available links)
#define NDIMS 3         // Cartesian mesh dimension
#define Hz 850.e6      // CPU clock rate, in Hz
#define LENGTH 1024      // message size, in doubles
#define L3CACHE 32     // last level cache in MB, used to flash the cache before each test


unsigned long long timebase();
void durand(double *, int *, double *);

main( int argc, char *argv[] )
{
    int taskid, ntasks, i, j;
    double sb[NDIMS][2][LENGTH], rb[NDIMS][2][LENGTH]; // buffers: 2 displacements in each dimension
    unsigned long long t1, t2, tdelay;
    int dims[NDIMS], periods[NDIMS], reorder;
    MPI_Comm comm_cart;
    MPI_Request req[2*NDIMS];
    MPI_Status  stt[2*NDIMS];
    double seed, delay;
    int one;
    useconds_t udelay;
    int rank_src[2][NDIMS], rank_dst[2][NDIMS]; // For positive displacement and dimension 1, source rank is rank_src[0][1], destination rank is rank_dst[0][1];
                                                // For negative displacement and dimension 0, source rank is rank_src[1][0], destination rank is rank_dst[1][0];
    char *src, *trg; // memcpy buffers used to flash last level cache
    size_t LB;

    LB = L3CACHE * 1024 * 1024;
    src = (char *)malloc( LB );
    trg = (char *)malloc( LB );
                                                
    MPI_Init( &argc, &argv );
    MPI_Comm_rank( MPI_COMM_WORLD, &taskid );
    MPI_Comm_size( MPI_COMM_WORLD, &ntasks );
    
    for ( i = 0; i < NDIMS; i++ ) dims[i] = 0;
    MPI_Dims_create( ntasks, NDIMS, dims );

    if ( taskid == 0 ) printf( "Cartesian topology: %d x %d x %d\n", dims[0], dims[1], dims[2] );

    for ( i = 0; i < NDIMS; i++ ) periods[i] = 0; // no periods for this test
    reorder = 1; // reorder is allowed
    MPI_Cart_create( MPI_COMM_WORLD, NDIMS, dims, periods, reorder, &comm_cart);

    // Generate disbalance and measure the longest delay
    seed = (double)taskid;
    one = 1;
    durand( &seed, &one, &delay );
    udelay = (useconds_t)(delay * 1e5 );
    
    MPI_Barrier( comm_cart );
    t1 = timebase();
    
    usleep( udelay );

    MPI_Barrier( comm_cart );
    t2 = timebase();
    /////////////////////////////////////////////////////

    tdelay = t2 - t1;
    //fprintf( stderr, "Hello from rank %d of %d tasks: delay %ld microseconds\n", taskid, ntasks, udelay );
    if ( taskid == 0 ) fprintf( stderr, "Delay time: %lld pclks, %18.12lf microseconds\n", 
        tdelay, (double)tdelay / Hz * 1e6 );
    
    
    for( i = 0; i < NDIMS; i++ )
    {
        MPI_Cart_shift( comm_cart, i,  1, &rank_src[0][i], &rank_dst[0][i] );
        MPI_Cart_shift( comm_cart, i, -1, &rank_src[1][i], &rank_dst[1][i] );
    }

    
    ///////////// Test Sendrecv without delay //////////////////
    memcpy( trg, src, LB );

    MPI_Barrier( comm_cart );
    t1 = timebase();

    for ( i = 0; i < NDIMS; i++ )
    {
        MPI_Sendrecv( &sb[i][0][0], LENGTH, MPI_DOUBLE, rank_dst[0][i], 0, &rb[i][0][0], LENGTH, MPI_DOUBLE, rank_src[0][i], 0, comm_cart, MPI_STATUS_IGNORE );
        MPI_Sendrecv( &sb[i][1][0], LENGTH, MPI_DOUBLE, rank_dst[1][i], 1, &rb[i][1][0], LENGTH, MPI_DOUBLE, rank_src[1][i], 1, comm_cart, MPI_STATUS_IGNORE );
    }
    
    MPI_Barrier( comm_cart );
    t2 = timebase();

    if( taskid == 0 ) fprintf( stderr, "Sendrecv no delay for %6d doubles: %lld pclks, %18.12lf microseconds\n",
        LENGTH, t2 - t1, (double)( t2 - t1 ) / Hz * 1e6 );

    //////////// Test Sendrecv with delay ////////////////////
    memcpy( trg, src, LB );
    
    MPI_Barrier( comm_cart );
    t1 = timebase();

    usleep( udelay );

    for ( i = 0; i < NDIMS; i++ )
    {
        MPI_Sendrecv( &sb[i][0][0], LENGTH, MPI_DOUBLE, rank_dst[0][i], 0, &rb[i][0][0], LENGTH, MPI_DOUBLE, rank_src[0][i], 0, comm_cart, MPI_STATUS_IGNORE );
        MPI_Sendrecv( &sb[i][1][0], LENGTH, MPI_DOUBLE, rank_dst[1][i], 1, &rb[i][1][0], LENGTH, MPI_DOUBLE, rank_src[1][i], 1, comm_cart, MPI_STATUS_IGNORE );
    }
    
    MPI_Barrier( comm_cart );
    t2 = timebase();

    if( taskid == 0 ) fprintf( stderr, "Sendrecv wt delay time for %6d doubles: %lld pclks, %18.12lf microseconds\n",
        LENGTH, t2 - t1 - tdelay, (double)( t2 - t1 - tdelay ) / Hz * 1e6 );


    ///////////// Test ISend - Recv - Barrier without delay //////////////////
    memcpy( trg, src, LB );

    MPI_Barrier( comm_cart );
    t1 = timebase();

    for ( i = 0; i < NDIMS; i++ )
    {
        for ( j = 0; j < 2; j++ ) // displacement
        {
            MPI_Isend( &sb[i][j][0], LENGTH, MPI_DOUBLE, rank_dst[j][i], 0, comm_cart, &req[0] ); 
            MPI_Recv ( &rb[i][j][0], LENGTH, MPI_DOUBLE, rank_src[j][i], 0, comm_cart, MPI_STATUS_IGNORE );
            MPI_Barrier( comm_cart );
        }
    }
    
    MPI_Barrier( comm_cart );
    t2 = timebase();

    if( taskid == 0 ) fprintf( stderr, "Isend-recv no delay for %6d doubles: %lld pclks, %18.12lf microseconds\n",
        LENGTH, t2 - t1, (double)( t2 - t1 ) / Hz * 1e6 );

    ///////////// Test ISend - Recv - Barrier with delay //////////////////
    memcpy( trg, src, LB );
    
    MPI_Barrier( comm_cart );
    t1 = timebase();

    usleep( udelay );

    for ( i = 0; i < NDIMS; i++ )
    {
        for ( j = 0; j < 2; j++ ) // displacement
        {
            MPI_Isend( &sb[i][j][0], LENGTH, MPI_DOUBLE, rank_dst[j][i], 0, comm_cart, &req[0] ); 
            MPI_Recv ( &rb[i][j][0], LENGTH, MPI_DOUBLE, rank_src[j][i], 0, comm_cart, MPI_STATUS_IGNORE );
            MPI_Barrier( comm_cart );
        }
    }
    
    MPI_Barrier( comm_cart );
    t2 = timebase();

    if( taskid == 0 ) fprintf( stderr, "Isend-recv wt delay for %6d doubles: %lld pclks, %18.12lf microseconds\n",
        LENGTH, t2 - t1 - tdelay, (double)( t2 - t1 - tdelay ) / Hz * 1e6 );

    ///////////// Test ISend - Recv - Wait without delay //////////////////
    memcpy( trg, src, LB );
    
    MPI_Barrier( comm_cart );
    t1 = timebase();

    for ( i = 0; i < NDIMS; i++ )
    {
        for ( j = 0; j < 2; j++ ) // displacement
        {
            MPI_Isend( &sb[i][j][0], LENGTH, MPI_DOUBLE, rank_dst[j][i], 0, comm_cart, &req[0] ); 
            MPI_Irecv( &rb[i][j][0], LENGTH, MPI_DOUBLE, rank_src[j][i], 0, comm_cart, &req[1] );
            MPI_Waitall( 2, &req[0], &stt[0] ); 
        }
    }
    
    MPI_Barrier( comm_cart );
    t2 = timebase();

    if( taskid == 0 ) fprintf( stderr, "Isend-Irecv no delay for %6d doubles: %lld pclks, %18.12lf microseconds\n",
        LENGTH, t2 - t1, (double)( t2 - t1 ) / Hz * 1e6 );


    ///////////// Test ISend - Recv - Wait with delay //////////////////
    memcpy( trg, src, LB );
    
    MPI_Barrier( comm_cart );
    t1 = timebase();

    usleep( udelay );

    for ( i = 0; i < NDIMS; i++ )
    {
        for ( j = 0; j < 2; j++ ) // displacement
        {
            MPI_Isend( &sb[i][j][0], LENGTH, MPI_DOUBLE, rank_dst[j][i], 0, comm_cart, &req[0] ); 
            MPI_Irecv( &rb[i][j][0], LENGTH, MPI_DOUBLE, rank_src[j][i], 0, comm_cart, &req[1] );
            MPI_Waitall( 2, &req[0], &stt[0] ); 
        }
    }
    
    MPI_Barrier( comm_cart );
    t2 = timebase();

    if( taskid == 0 ) fprintf( stderr, "Isend-Irecv wt delay for %6d doubles: %lld pclks, %18.12lf microseconds\n",
        LENGTH, t2 - t1 - tdelay, (double)( t2 - t1 - tdelay ) / Hz * 1e6 );

    ///////////// Test ISend - Recv - Wait all 6 without delay //////////////////
    memcpy( trg, src, LB );
    
    MPI_Barrier( comm_cart );
    t1 = timebase();

    for ( i = 0; i < NDIMS; i++ )
    {
        MPI_Isend( &sb[i][0][0], LENGTH, MPI_DOUBLE, rank_dst[0][i], 0, comm_cart, &req[i*4+0] ); 
        MPI_Irecv( &rb[i][0][0], LENGTH, MPI_DOUBLE, rank_src[0][i], 0, comm_cart, &req[i*4+1] );
        
        MPI_Isend( &sb[i][1][0], LENGTH, MPI_DOUBLE, rank_dst[1][i], 0, comm_cart, &req[i*4+2] ); 
        MPI_Irecv( &rb[i][1][0], LENGTH, MPI_DOUBLE, rank_src[1][i], 0, comm_cart, &req[i*4+3] );
    }
    
    MPI_Waitall( 2*NDIMS, &req[0], &stt[0] ); 
    
    MPI_Barrier( comm_cart );
    t2 = timebase();

    if( taskid == 0 ) fprintf( stderr, "12 at a time no delay for %6d doubles: %lld pclks, %18.12lf microseconds\n",
        LENGTH, t2 - t1, (double)( t2 - t1 ) / Hz * 1e6 );

    ///////////// Test ISend - Recv - Wait all 6 with delay //////////////////
    memcpy( trg, src, LB );
    
    MPI_Barrier( comm_cart );
    t1 = timebase();

    usleep( udelay );

    for ( i = 0; i < NDIMS; i++ )
    {
        MPI_Isend( &sb[i][0][0], LENGTH, MPI_DOUBLE, rank_dst[0][i], 0, comm_cart, &req[i*4+0] ); 
        MPI_Irecv( &rb[i][0][0], LENGTH, MPI_DOUBLE, rank_src[0][i], 0, comm_cart, &req[i*4+1] );
        
        MPI_Isend( &sb[i][1][0], LENGTH, MPI_DOUBLE, rank_dst[1][i], 0, comm_cart, &req[i*4+2] ); 
        MPI_Irecv( &rb[i][1][0], LENGTH, MPI_DOUBLE, rank_src[1][i], 0, comm_cart, &req[i*4+3] );
    }
    
    MPI_Waitall( 2*NDIMS, &req[0], &stt[0] ); 
    
    MPI_Barrier( comm_cart );
    t2 = timebase();

    if( taskid == 0 ) fprintf( stderr, "12 at a time wt delay for %6d doubles: %lld pclks, %18.12lf microseconds\n",
        LENGTH, t2 - t1 - tdelay, (double)( t2 - t1 - tdelay ) / Hz * 1e6 );

    MPI_Finalize();

    free( src );
    free( trg );
}
