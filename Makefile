#FF      = mpixlf90
FF     = /bgsys/drivers/ppcfloor/comm/fast/bin/mpixlf77
CC     = /bgsys/drivers/ppcfloor/comm/fast/bin/mpixlc
LD     = $(CC)
FFLAGS = -g 
CFLAGS = -g -I/bgsys/drivers/ppcfloor/arch/include #-qnostaticlink
LDFLAGS = $(CFLAGS)
LIB    = -L$(HOME)/lib -ltimebase

TARGET = mmps
OBJS =  main.o durand.o

all: grid

%.o : %.f
	$(FF) $(FFLAGS) -c $<

%.o : %.c
	$(CC) $(CFLAGS) -c $<

grid: $(OBJS)
	$(LD) $(LDFLAGS) -o $(TARGET) $(OBJS) $(LIB)
        
clean:
	rm -f $(TARGET) $(OBJS)

