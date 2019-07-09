// clang -g -O2 -std=c11 -Wall -framework ApplicationServices disable-grayscale.c -o disable-grayscale
// https://stackoverflow.com/questions/14163788/how-does-on-screen-color-inversion-work-in-os-x
#include <stdio.h>
#include <ApplicationServices/ApplicationServices.h>

CG_EXTERN bool CGDisplayUsesForceToGray(void);
CG_EXTERN void CGDisplayForceToGray(bool forceToGray);

int
main(int argc, char** argv)
{
    bool isGrayscale = CGDisplayUsesForceToGray();
		if (isGrayscale) {
	    CGDisplayForceToGray(FALSE);
		}

    return 0;
}