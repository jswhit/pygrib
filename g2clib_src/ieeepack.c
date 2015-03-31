#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <endian.h>
#include "grib2.h"


void ieeepack(g2float *fld,g2int ndpts,g2int *idrstmpl,unsigned char *cpack,g2int *lcpack)
//$$$  SUBPROGRAM DOCUMENTATION BLOCK
//                .      .    .                                       .
// SUBPROGRAM:    ieeepack
//   PRGMMR: Roux          ORG: W/NP11    DATE: 2014-04-01
//
// ABSTRACT: This subroutine packs up a data field using the ieee
//   packing algorithm as defined in the GRIB2 documention.  It
//   also fills in GRIB2 Data Representation Template 5.4 with the
//   appropriate values.
//
// PROGRAM HISTORY LOG:
// 2014-04-01  Roux
//
// USAGE:    CALL ieeepack(fld,ndpts,idrstmpl,cpack,lcpack)
//   INPUT ARGUMENT LIST:
//     fld[]    - Contains the data values to pack
//     ndpts    - The number of data values in array fld[]
//     idrstmpl - Contains the array of values for Data Representation
//                Template 5.4
//                [0] = Precision (See code Table 5.7)
//                      1 IEEE 32-bit 
//                      2 IEEE 64-bit
//                      3 IEEE 128-bit
//   OUTPUT ARGUMENT LIST: 
//     cpack    - The packed data field
//     lcpack   - length of packed field starting at cpack.
//
// REMARKS: None
//
// ATTRIBUTES:
//   LANGUAGE: C
//   MACHINE:  
//
//$$$
{
     float ftmp;
     double dtmp;
     uint32_t *ptr32a, *ptr32b;
     uint64_t *ptr64a, *ptr64b;
     int i;
      if (idrstmpl[0] == 1 ) {
         printf("Packing %d single-precision values\n");
         *lcpack = ndpts*4;
         ptr32a = (uint32_t *) &ftmp;
         ptr32b = (uint32_t *) cpack;
         for (i=0;i<=ndpts;i++) {
            ftmp = fld[i];
            ptr32b[i] = htobe32(*ptr32a);
         }
      }
      else if (idrstmpl[0] == 2 ) {
         *lcpack = ndpts*8;
         ptr64a = (uint64_t *) &dtmp;
         ptr64b = (uint64_t *) cpack;
         for (i=0;i<=ndpts;i++) {
            dtmp = fld[i];
            ptr64b[i] = htobe64(*ptr64a);
         }
      } else {
        *lcpack=0;
        printf("Oooops! Can't handle precision code other than 1 or 2..  %d given..\n",idrstmpl[0]);
        return;
      }
      printf("Packing over\n");
}
