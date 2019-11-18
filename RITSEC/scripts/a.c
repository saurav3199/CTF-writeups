#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
    unsigned int numbers[] = {atoi(argv[1]), atoi(argv[2]), atoi(argv[3]),atoi(argv[4]), atoi(argv[5])};
    unsigned int r,t=time(0),j=4;
    for(int i = 0; i < 1000000; i++)
    {
        srand(t - i);
        r=rand();
        if(r!=numbers[0])
            continue;
        while(j-->0)
        {
            rand();
        }
        printf("%d\n",rand());
        break;
    }
    return 0;
}