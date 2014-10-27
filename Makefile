#FF      = mpixlf90
FF     = /bgsys/drivers/ppcfloor/comm/fast/bin/mpixlf77
CC     = /bgsys/drivers/ppcfloor/comm/fast/bin/mpixlc
LD     = $(CC)

CINCLUDE  = -I/bgsys/drivers/ppcfloor 
CINCLUDE += -I/bgsys/drivers/ppcfloor/firmware/include
CINCLUDE += -I/bgsys/drivers/ppcfloor/spi/include/kernel 
CINCLUDE += -I/bgsys/drivers/ppcfloor/spi/include/kernel/cnk
CINCLUDE += -I/bgsys/drivers/ppcfloor/arch/include

FFLAGS = -g 
CFLAGS = -g $(CINCLUDE) #-qnostaticlink
LDFLAGS = $(CFLAGS)
LIB    = -L$(HOME)/lib -ltimebase

TARGET = mmps
OBJS =  main.o durand.o q5d.o

all: grid

%.o : %.f
	$(FF) $(FFLAGS) -c $<

%.o : %.c
	$(CC) $(CFLAGS) -c $<

grid: $(OBJS)
	$(LD) $(LDFLAGS) -o $(TARGET) $(OBJS) $(LIB)
        
clean:
	rm -f $(TARGET) $(OBJS)

