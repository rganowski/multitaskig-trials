#include <stdio.h>
#include <omp.h>

int main()
{
    const int DATA[19] = {10, 9, 4, 15, 2, 9, 13, 10, 8, 8, 22, 6, 3, 8, 4, 12, 5, 9, 12};
    int NUM_ELEMS = sizeof(DATA) / sizeof(DATA[0]);

    printf("index: ");
    for (int i = 0; i < NUM_ELEMS; i++)
    {
        printf("| %3d ", i);
    }
    printf("|\nvalue: ");
    for (int i = 0; i < NUM_ELEMS; i++)
    {
        printf("| %3d ", DATA[i]);
    }
    printf("|\n\n");

    int subtotal = 0, total = 0;
    printf("|   p |  counter (i) |  in subtotal | out subtotal |\n");
    printf("| --- | ------------ | ------------ | ------------ |\n");

#pragma omp parallel private(subtotal)
    {

#pragma omp for
        for (int i = 0; i < NUM_ELEMS; i++)
        {
            int new_subtotal = subtotal + DATA[i];
            int p = omp_get_thread_num() + 1;
            printf("| %3d | %12d | %12d | %12d |\n", p, i, subtotal, new_subtotal);
            subtotal = new_subtotal;
        }

#pragma omp critical
        total += subtotal;
    }
    printf("| --- | ------------ | ------------ | ------------ |\n");
    printf("                             TOTAL: | %12d |\n", total);
}