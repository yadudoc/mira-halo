#FF      = mpixlf90

ifeq ($(HALO_SYS),)
	HALO_SYS := bgq
endif

ifeq ($(HALO_SYS),crayxe6)
	FF     = ftn
	CC     = cc
	LD     = $(CC)
else ifeq ($(HALO_SYS),bgq)
	FF     = /bgsys/drivers/ppcfloor/comm/fast/bin/mpixlf77
	CC     = /bgsys/drivers/ppcfloor/comm/fast/bin/mpixlc
	LD     = $(CC)
else ifeq ($(HALO_SYS),gnu)
	FF     = mpif90
	CC     = mpicc
	LD     = $(CC)
else
	CC     = $(error Bad HALO_SYS: $(HALO_SYS))
	FF     = $(CC)
	LD     = $(CC)
endif


CINCLUDE :=
ifeq ($(HALO_SYS),crayxe6)
	# TODO
	CINCLUDE +=
else ifeq ($(HALO_SYS),bgq)
	CINCLUDE  = -I/bgsys/drivers/ppcfloor
	CINCLUDE += -I/bgsys/drivers/ppcfloor/firmware/include
	CINCLUDE += -I/bgsys/drivers/ppcfloor/spi/include/kernel
	CINCLUDE += -I/bgsys/drivers/ppcfloor/spi/include/kernel/cnk
	CINCLUDE += -I/bgsys/drivers/ppcfloor/arch/include
endif

FFLAGS = -g
CFLAGS = -g $(CINCLUDE) -Wall #-qnostaticlink
LDFLAGS = $(CFLAGS)
LIB =

ifeq ($(HALO_SYS),crayxe6)
	FFLAGS += -fno-underscoring
        CFLAGS += -D HALO_CRAYXE6
	LIB +=
else ifeq ($(HALO_SYS),bgq)
        CFLAGS += -D HALO_BGQ
	LIB += -L$(HOME)/lib -ltimebase
else ifeq ($(HALO_SYS),gnu)
	FFLAGS += -fno-underscoring
        CFLAGS += -D HALO_GNU
	LIB += -lgfortran
endif

TARGET = mmps
OBJS =  main.o durand.o

ifeq ($(HALO_SYS),bgq)
  OBJS += q5d.o
endif

all: grid

%.o : %.f
	$(FF) $(FFLAGS) -c $<

%.o : %.c
	$(CC) $(CFLAGS) -c $<

grid: $(OBJS)
	$(LD) $(LDFLAGS) -o $(TARGET) $(OBJS) $(LIB)
	
clean:
	rm -f $(TARGET) $(OBJS)

