#include <stdlib.h>
#include "grib2.h"
#include "pdstemplates.h"

g2int getpdsindex(g2int number)
///$$$  SUBPROGRAM DOCUMENTATION BLOCK
//                .      .    .                                       .
// SUBPROGRAM:    getpdsindex
//   PRGMMR: Gilbert         ORG: W/NP11    DATE: 2001-06-28
//
// ABSTRACT: This function returns the index of specified Product
//   Definition Template 4.NN (NN=number) in array templates.
//
// PROGRAM HISTORY LOG:
// 2001-06-28  Gilbert
// 2009-01-14  Vuong     Changed structure name template to gtemplate
// 2009-12-15  Vuong     Added Product Definition Template 4.31
//                       Added Product Definition Template 4.15
// 2010-08-03  Vuong     Added Product Definition Template 4.42 and 4.43
// 2010-12-08  Vuong     Corrected Product Definition Template 4.42 and 4.43
// 2012-03-29  Vuong     Added Templates 4.44,4.45,4.46,4.47,4.48,4.50,
//                       4.51,4.91,4.32 and 4.52
// 2013-08-05  Vuong     Corrected 4.91 and added Templates 4.33,4.34,4.53,4.54
// 2015-10-07  Vuong     Added Templates 4.57, 4.60, 4.61 and
//                       allow a forecast time to be negative
// USAGE:    index=getpdsindex(number)
//   INPUT ARGUMENT LIST:
//     number   - NN, indicating the number of the Product Definition
//                Template 4.NN that is being requested.
//
// RETURNS:  Index of PDT 4.NN in array templates, if template exists.
//           = -1, otherwise.
//
// REMARKS: None
//
// ATTRIBUTES:
//   LANGUAGE: C
//   MACHINE:  IBM SP
//
//$$$/
{
           g2int j,getpdsindex=-1;

           for (j=0;j<MAXPDSTEMP;j++) {
              if (number == templatespds[j].template_num) {
                 getpdsindex=j;
                 return(getpdsindex);
              }
           }

           return(getpdsindex);
}


gtemplate *getpdstemplate(g2int number)
///$$$  SUBPROGRAM DOCUMENTATION BLOCK
//                .      .    .                                       .
// SUBPROGRAM:    getpdstemplate 
//   PRGMMR: Gilbert         ORG: W/NP11    DATE: 2000-05-11
//
// ABSTRACT: This subroutine returns PDS template information for a 
//   specified Product Definition Template 4.NN.
//   The number of entries in the template is returned along with a map
//   of the number of octets occupied by each entry.  Also, a flag is
//   returned to indicate whether the template would need to be extended.
//
// PROGRAM HISTORY LOG:
// 2000-05-11  Gilbert
// 2009-01-14  Vuong     Changed structure name template to gtemplate
// 2009-08-05  Vuong     Added Product Definition Template 4.31
// 2010-08-03  Vuong     Added Product Definition Template 4.42 and 4.43
// 2010-12-08  Vuong     Corrected Product Definition Template 4.42 and 4.43
// 2012-02-15  Vuong     Added Templates 4.44,4.45,4.46,4.47,4.48,4.50,
//                       4.51,4.91,4.32 and 4.52
// 2013-08-05  Vuong     Corrected 4.91 and added Templates 4.33,4.34,4.53,4.54
// 2015-10-07  Vuong     Added Templates 4.57, 4.60, 4.61 and
//                       allow a forecast time to be negative
//
// USAGE:    CALL getpdstemplate(number)
//   INPUT ARGUMENT LIST:
//     number   - NN, indicating the number of the Product Definition 
//                Template 4.NN that is being requested.
//
//   RETURN VALUE:
//        - Pointer to the returned template struct.
//          Returns NULL pointer, if template not found.
//
// REMARKS: None
//
// ATTRIBUTES:
//   LANGUAGE: C
//   MACHINE:  IBM SP
//
//$$$/
{
           g2int index;
           gtemplate *new;

           index=getpdsindex(number);

           if (index != -1) {
              new=(gtemplate *)malloc(sizeof(gtemplate));
              new->type=4;
              new->num=templatespds[index].template_num;
              new->maplen=templatespds[index].mappdslen;
              new->needext=templatespds[index].needext;
              new->map=(g2int *)templatespds[index].mappds;
              new->extlen=0;
              new->ext=0;        //NULL
              return(new);
           }
           else {
             printf("getpdstemplate: PDS Template 4.%d not defined.\n",(int)number);
             return(0);        //NULL
           }

         return(0);        //NULL
}
         
        
gtemplate *extpdstemplate(g2int number,g2int *list)
///$$$  SUBPROGRAM DOCUMENTATION BLOCK
//                .      .    .                                       .
// SUBPROGRAM:    extpdstemplate 
//   PRGMMR: Gilbert         ORG: W/NP11    DATE: 2000-05-11
//
// ABSTRACT: This subroutine generates the remaining octet map for a
//   given Product Definition Template, if required.  Some Templates can
//   vary depending on data values given in an earlier part of the 
//   Template, and it is necessary to know some of the earlier entry
//   values to generate the full octet map of the Template.
//
// PROGRAM HISTORY LOG:
// 2000-05-11  Gilbert
// 2009-01-14  Vuong     Changed structure name template to gtemplate
// 2009-08-05  Vuong     Added Product Definition Template 4.31
// 2010-08-03  Vuong     Added Product Definition Template 4.42 and 4.43
// 2010-12-08  Vuong     Corrected Product Definition Template 4.42 and 4.43
// 2012-02-15  Vuong     Added Templates 4.44,4.45,4.46,4.47,4.48,4.50,
//                       4.51,4.91,4.32 and 4.52
// 2013-08-05  Vuong     Corrected 4.91 and added Templates 4.33,4.34,4.53,4.54
// 2015-10-07  Vuong     Added Templates 4.57, 4.60, 4.61 and
//                       allow a forecast time to be negative
//
// USAGE:    CALL extpdstemplate(number,list)
//   INPUT ARGUMENT LIST:
//     number   - NN, indicating the number of the Product Definition 
//                Template 4.NN that is being requested.
//     list()   - The list of values for each entry in the 
//                the Product Definition Template 4.NN.
//
//   RETURN VALUE:
//        - Pointer to the returned template struct.
//          Returns NULL pointer, if template not found.
//
// ATTRIBUTES:
//   LANGUAGE: C
//   MACHINE:  IBM SP
//
//$$$
{
           gtemplate *new;
           g2int index,i,j,k,l;

           index=getpdsindex(number);
           if (index == -1) return(0);

           new=getpdstemplate(number);

           if ( ! new->needext ) return(new);

           if ( number == 3 ) {
              new->extlen=list[26];
              new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
              for (i=0;i<new->extlen;i++) {
                 new->ext[i]=1;
              }
           }
           else if ( number == 4 ) {
              new->extlen=list[25];
              new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
              for (i=0;i<new->extlen;i++) {
                 new->ext[i]=1;
              }
           }
           else if ( number == 8 ) {
              if ( list[21] > 1 ) {
                 new->extlen=(list[21]-1)*6;
                 new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
                 for (j=2;j<=list[21];j++) {
                    l=(j-2)*6;
                    for (k=0;k<6;k++) {
                       new->ext[l+k]=new->map[23+k];
                    }
                 }
              }
           }
           else if ( number == 9 ) {
              if ( list[28] > 1 ) {
                 new->extlen=(list[28]-1)*6;
                 new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
                 for (j=2;j<=list[28];j++) {
                    l=(j-2)*6;
                    for (k=0;k<6;k++) {
                       new->ext[l+k]=new->map[30+k];
                    }
                 }
              }
           }
           else if ( number == 10 ) {
              if ( list[22] > 1 ) {
                 new->extlen=(list[22]-1)*6;
                 new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
                 for (j=2;j<=list[22];j++) {
                    l=(j-2)*6;
                    for (k=0;k<6;k++) {
                       new->ext[l+k]=new->map[24+k];
                    }
                 }
              }
           }
           else if ( number == 11 ) {
              if ( list[24] > 1 ) {
                 new->extlen=(list[24]-1)*6;
                 new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
                 for (j=2;j<=list[24];j++) {
                    l=(j-2)*6;
                    for (k=0;k<6;k++) {
                       new->ext[l+k]=new->map[26+k];
                    }
                 }
              }
           }
           else if ( number == 12 ) {
              if ( list[23] > 1 ) {
                 new->extlen=(list[23]-1)*6;
                 new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
                 for (j=2;j<=list[23];j++) {
                    l=(j-2)*6;
                    for (k=0;k<6;k++) {
                       new->ext[l+k]=new->map[25+k];
                    }
                 }
              }
           }
           else if ( number == 13 ) {
              new->extlen=((list[37]-1)*6)+list[26];
              new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
              if ( list[37] > 1 ) {
                 for (j=2;j<=list[37];j++) {
                    l=(j-2)*6;
                    for (k=0;k<6;k++) {
                       new->ext[l+k]=new->map[39+k];
                    }
                 }
              }
              l=(list[37]-1)*6;
              if ( l<0 ) l=0;
              for (i=0;i<list[26];i++) {
                new->ext[l+i]=1;
              }
           }
           else if ( number == 14 ) {
              new->extlen=((list[36]-1)*6)+list[25];
              new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
              if ( list[36] > 1 ) {
                 for (j=2;j<=list[36];j++) {
                    l=(j-2)*6;
                    for (k=0;k<6;k++) {
                       new->ext[l+k]=new->map[38+k];
                    }
                 }
              }
              l=(list[36]-1)*6;
              if ( l<0 ) l=0;
              for (i=0;i<list[25];i++) {
                new->ext[l+i]=1;
              }
           }
           else if ( number == 30 ) {
              new->extlen=list[4]*5;
              new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
              for (i=0;i<list[4];i++) {
                 l=i*5;
                 new->ext[l]=2;
                 new->ext[l+1]=2;
                 new->ext[l+2]=1;
                 new->ext[l+3]=1;
                 new->ext[l+4]=4;
              }
           }
           else if ( number == 31 ) {
              new->extlen=list[4]*5;
              new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
              for (i=0;i<list[4];i++) {
                 l=i*5;
                 new->ext[l]=2;
                 new->ext[l+1]=2;
                 new->ext[l+2]=2;
                 new->ext[l+3]=1;
                 new->ext[l+4]=4;
              }
           }
           else if ( number == 42 ) {
              if ( list[22] > 1 ) {
                 new->extlen=(list[22]-1)*6;
                 new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
                 for (j=2;j<=list[22];j++) {
                    l=(j-2)*6;
                    for (k=0;k<6;k++) {
                       new->ext[l+k]=new->map[24+k];
                    }
                 }
              }
           }
           else if ( number == 43 ) {
              if ( list[25] > 1 ) {
                 new->extlen=(list[25]-1)*6;
                 new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
                 for (j=2;j<=list[25];j++) {
                    l=(j-2)*6;
                    for (k=0;k<6;k++) {
                       new->ext[l+k]=new->map[27+k];
                    }
                 }
              }
           }
           else if ( number == 32 ) {
              new->extlen=list[9]*10;
              new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
              for (i=0;i<list[9];i++) {
                 l=i*5;
                 new->ext[l]=2;
                 new->ext[l+1]=2;
                 new->ext[l+2]=2;
                 new->ext[l+3]=-1;
                 new->ext[l+4]=-4;
              }
           }
           else if ( number == 46 ) {
              if ( list[27] > 1 ) {
                 new->extlen=(list[27]-1)*6;
                 new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
                 for (j=2;j<=list[27];j++) {
                    l=(j-2)*6;
                    for (k=0;k<6;k++) {
                       new->ext[l+k]=new->map[29+k];
                    }
                 }
              }
           }
           else if ( number == 47 ) {
              if ( list[30] > 1 ) {
                 new->extlen=(list[30]-1)*6;
                 new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
                 for (j=2;j<=list[30];j++) {
                    l=(j-2)*6;
                    for (k=0;k<6;k++) {
                       new->ext[l+k]=new->map[32+k];
                    }
                 }
              }
           else if ( number == 51 ) {
              new->extlen=list[15]*11;
              new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
              for (i=0;i<list[15];i++) {
                 l=i*6;
                 new->ext[l]=1;
                 new->ext[l+1]=1;
                 new->ext[l+2]=-1;
                 new->ext[l+3]=-4;
                 new->ext[l+4]=-1;
                 new->ext[l+5]=-4;
              }
           }
           else if ( number == 33 ) {
              new->extlen=list[9];
              new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
              for (i=0;i<new->extlen;i++) {
                 new->ext[i]=1;
              }
           }
           else if ( number == 34 ) {
              new->extlen=((list[24]-1)*6)+list[9];
              new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
              if ( list[24] > 1 ) {
                 for (j=2;j<=list[24];j++) {
                    l=(j-2)*6;
                    for (k=0;k<6;k++) {
                       new->ext[l+k]=new->map[26+k];
                    }
                 }
              }
              l=(list[24]-1)*6;
              if ( l<0 ) l=0;
              for (i=0;i<list[9];i++) {
                new->ext[l+i]=1;
              }
           }
           else if ( number == 53 ) {
              new->extlen=list[3];
              new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
              for (i=0;i<new->extlen;i++) {
                 new->ext[i]=1;
              }
           }
           else if ( number == 54 ) {
              new->extlen=list[3];
              new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
              for (i=0;i<new->extlen;i++) {
                 new->ext[i]=1;
              }
           }
           else if ( number == 91 ) {
              new->extlen=((list[28]-1)*6)+list[15];
              new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
              if ( list[28] > 1 ) {
                 for (j=2;j<=list[28];j++) {
                    l=(j-2)*6;
                    for (k=0;k<6;k++) {
                       new->ext[l+k]=new->map[30+k];
                    }
                 }
              }
              l=(list[29]-1)*6;
              if ( l<0 ) l=0;
              for (i=0;i<list[15];i++) {
                new->ext[l+i]=1;
              }
             }
// PDT 4.57  (10/07/2015)
           else if ( number == 57 ) {
              new->extlen=list[6]*15;
              new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
              for (i=0;i<list[6];i++) {
                 l=i*15;
                 new->ext[l]=1;
                 new->ext[l+1]=-4;
                 new->ext[l+2]=1;
                 new->ext[l+3]=1;
                 new->ext[l+4]=1;
                 new->ext[l+5]=2;
                 new->ext[l+6]=1;
                 new->ext[l+7]=1;
                 new->ext[l+8]=-4;
                 new->ext[l+9]=1;
                 new->ext[l+10]=-1;
                 new->ext[l+11]=-4;
                 new->ext[l+12]=1;
                 new->ext[l+13]=-1;
                 new->ext[l+14]=-4;
              }
           }
// PDT 4.61  (10/07/2015)
           else if ( number == 61 ) {
              if ( list[30] > 1 ) {
                 new->extlen=(list[30]-1)*6;
                 new->ext=(g2int *)malloc(sizeof(g2int)*new->extlen);
                 for (j=2;j<=list[30];j++) {
                    l=(j-2)*6;
                    for (k=0;k<6;k++) {
                       new->ext[l+k]=new->map[32+k];
                    }
                 }
              }
           }

           }

           return(new);

}
