#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <endian.h>
#include "grib2.h"


g2int ieeeunpack(unsigned char *cpack,g2int *idrstmpl,g2int ndpts,g2float *fld)
//$$$  SUBPROGRAM DOCUMENTATION BLOCK
//                .      .    .                                       .
// SUBPROGRAM:    ieeeunpack
//   PRGMMR: Roux          ORG: W/NP11    DATE: 2014-04-01
//
// ABSTRACT: This subroutine unpacks a data field that was packed using the ieee
//   packing algorithm as defined in the GRIB2 documention,
//   using info from the GRIB2 Data Representation Template 5.4.
//
// PROGRAM HISTORY LOG:
// 2014-04-01  Roux
//
// USAGE:    int ieeeunpack(unsigned char *cpack,g2int *idrstmpl,g2int ndpts,
//                         g2float *fld)
//   INPUT ARGUMENT LIST:
//     cpack    - pointer to the packed data field.
//     idrstmpl - pointer to the array of values for Data Representation
//                Template 5.4
//     ndpts    - The number of data values to unpack
//
//   OUTPUT ARGUMENT LIST:
//     fld      - Contains the unpacked data values.  fld must be allocated
//                with at least ndpts*sizeof(g2float) bytes before
//                calling this routine.
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
         ptr32a = (uint32_t *) &ftmp;
         ptr32b = (uint32_t *) cpack;
         for (i=0;i<=ndpts;i++) {
            *ptr32a = be32toh(ptr32b[i]);
            fld[i] = ftmp;
         }
      }
      else if (idrstmpl[0] == 2 ) {
         ptr64a = (uint64_t *) &dtmp;
         ptr64b = (uint64_t *) cpack;
         for (i=0;i<=ndpts;i++) {
            *ptr64a = be64toh(ptr64b[i]);
            fld[i] = dtmp;
         }
      } else {
        printf("Oooops! Can't handle precision code other than 1 or 2..  %d given..\n",idrstmpl[0]);
        return(-1);
      }
      return(0);
}
