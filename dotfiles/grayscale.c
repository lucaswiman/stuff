// clang -g -O2 -std=c11 -Wall -framework ApplicationServices -o toggle-grayscale
// https://stackoverflow.com/questions/14163788/how-does-on-screen-color-inversion-work-in-os-x
#include <stdio.h>
#include <ApplicationServices/ApplicationServices.h>

CG_EXTERN bool CGDisplayUsesForceToGray(void);
CG_EXTERN void CGDisplayForceToGray(bool forceToGray);

int
main(int argc, char** argv)
{
    bool isGrayscale = CGDisplayUsesForceToGray();
    printf("isGrayscale = %d\n", isGrayscale);
    CGDisplayForceToGray(!isGrayscale);
    printf("Grayscale is now: %d\n", CGDisplayUsesForceToGray());

    return 0;
}