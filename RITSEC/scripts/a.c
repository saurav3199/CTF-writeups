#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
    unsigned int seq[] = {atoi(argv[1]), atoi(argv[2]), atoi(argv[3]),\
        atoi(argv[4]), atoi(argv[5])};
    unsigned int r;
    for(int i = 0; i < 1000000; i++)
    {
        srand(time(0) - i);
        for(int j = 0; j < 5; j++)
        {    
            r = rand();
            if(r != seq[j])
            {
                break;
            }
            if(j == 4)
            {
                printf("%d %d\n", i,rand());
                exit(0);
            }
        }
    }
    exit(1);
    return 0;
}