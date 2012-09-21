#ifndef _pdstemplates_H
#define _pdstemplates_H
#include "grib2.h"

//   PRGMMR: Gilbert         ORG: W/NP11    DATE: 2002-10-26
//
// ABSTRACT: This inculde file contains info on all the available 
//   GRIB2 Product Definition Templates used in Section 4 (PDS).
//   The information decribing each template is stored in the
//   pdstemplate structure defined below.
//
//   Each Template has three parts: The number of entries in the template
//   (mappdslen);  A map of the template (mappds), which contains the
//   number of octets in which to pack each of the template values; and
//   a logical value (needext) that indicates whether the Template needs 
//   to be extended.  In some cases the number of entries in a template 
//   can vary depending upon values specified in the "static" part of 
//   the template.  ( See Template 4.3 as an example )
//
//   NOTE:  Array mappds contains the number of octets in which the 
//   corresponding template values will be stored.  A negative value in
//   mappds is used to indicate that the corresponding template entry can
//   contain negative values.  This information is used later when packing
//   (or unpacking) the template data values.  Negative data values in GRIB
//   are stored with the left most bit set to one, and a negative number
//   of octets value in mappds[] indicates that this possibility should
//   be considered.  The number of octets used to store the data value
//   in this case would be the absolute value of the negative value in 
//   mappds[].
//  
// 2005-12-08  Gilbert   Allow negative scale factors and limits for
//                       Templates 4.5 and 4.9
// 2009-12-15  Vuong     Added Product Definition Template 4.31
//                       Added Product Definition Template 4.15
// 2010-08-03  Vuong     Added Product Definition Template 4.40,4.41,4.42,4.43
// 2010-12-08  Vuong     Corrected Definition Template 4.42,4.43
// 2010-12-08  Vuong     Corrected Definition Template 4.42,4.43
// 2012-03-29  Vuong     Added Templates 4.44,4.45,4.46,4.47,4.48,4.50,
//                       4.51,4.91,4.32 and 4.52
//
//$$$

      #define MAXPDSTEMP 39           // maximum number of templates
      #define MAXPDSMAPLEN 200        // maximum template map length

      struct pdstemplate 
      {
          g2int template_num;
          g2int mappdslen;
          g2int needext;
          g2int mappds[MAXPDSMAPLEN];
      };

      const struct pdstemplate templatespds[MAXPDSTEMP] = {
             // 4.0: Analysis or Forecast at Horizontal Level/Layer
             //      at a point in time
         {0,15,0, {1,1,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4} },
             // 4.1: Individual Ensemble Forecast at Horizontal Level/Layer
             //      at a point in time
         {1,18,0, {1,1,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4,1,1,1} },
             // 4.2: Derived Fcst based on whole Ensemble at Horiz Level/Layer
             //      at a point in time
         {2,17,0, {1,1,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4,1,1} },
             // 4.3: Derived Fcst based on Ensemble cluster over rectangular
             //      area at Horiz Level/Layer at a point in time
         {3,31,1, {1,1,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4,1,1,1,1,1,1,1,-4,-4,4,4,1,-1,4,-1,4} },
             // 4.4: Derived Fcst based on Ensemble cluster over circular
             //      area at Horiz Level/Layer at a point in time
         {4,30,1, {1,1,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4,1,1,1,1,1,1,1,-4,4,4,1,-1,4,-1,4} },
             // 4.5: Probablility Forecast at Horiz Level/Layer
             //      at a point in time
         {5,22,0, {1,1,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4,1,1,1,-1,-4,-1,-4} },
             // 4.6: Percentile Forecast at Horiz Level/Layer
             //      at a point in time
         {6,16,0, {1,1,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4,1} },
             // 4.7: Analysis or Forecast Error at Horizontal Level/Layer
             //      at a point in time
         {7,15,0, {1,1,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4} },
             // 4.8: Ave/Accum/etc... at Horiz Level/Layer
             //      in a time interval
         {8,29,1, {1,1,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4,2,1,1,1,1,1,1,4,1,1,1,4,1,4} },
             // 4.9: Probablility Forecast at Horiz Level/Layer
             //      in a time interval
         {9,36,1, {1,1,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4,1,1,1,-1,-4,-1,-4,2,1,1,1,1,1,1,4,1,1,1,4,1,4} },
             // 4.10: Percentile Forecast at Horiz Level/Layer
             //       in a time interval
         {10,30,1, {1,1,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4,1,2,1,1,1,1,1,1,4,1,1,1,4,1,4} },
             // 4.11: Individual Ensemble Forecast at Horizontal Level/Layer
             //       in a time interval
         {11,32,1, {1,1,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4,1,1,1,2,1,1,1,1,1,1,4,1,1,1,4,1,4} },
             // 4.12: Derived Fcst based on whole Ensemble at Horiz Level/Layer
             //       in a time interval
         {12,31,1, {1,1,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4,1,1,2,1,1,1,1,1,1,4,1,1,1,4,1,4} },
             // 4.13: Derived Fcst based on Ensemble cluster over rectangular
             //       area at Horiz Level/Layer in a time interval
         {13,45,1, {1,1,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4,1,1,1,1,1,1,1,-4,-4,4,4,1,-1,4,-1,4,2,1,1,1,1,1,1,4,1,1,1,4,1,4} },
             // 4.14: Derived Fcst based on Ensemble cluster over circular
             //       area at Horiz Level/Layer in a time interval
         {14,44,1, {1,1,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4,1,1,1,1,1,1,1,-4,4,4,1,-1,4,-1,4,2,1,1,1,1,1,1,4,1,1,1,4,1,4} },
             // 4.15: Average, accumulation, extreme values or other statistically-processed values over a
             // spatial area at a horizontal level or in a horizontal layer at a point in time
         {15,18,0, {1,1,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4,1,1,1} },
             // 4.20: Radar Product
         {20,19,0, {1,1,1,1,1,-4,4,2,4,2,1,1,1,1,1,2,1,3,2} },
             // 4.30: Satellite Product
         {30,5,1, {1,1,1,1,1} },
             // 4.31: Satellite Product
         {31,5,1, {1,1,1,1,1} },
             // 4.40: Analysis or forecast at a horizontal level or in a horizontal layer
             // at a point in time for atmospheric chemical constituents
         {40,16,0, {1,1,2,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4} },
             // 4.41: Individual ensemble forecast, control and perturbed, at a horizontal level or
             // in a horizontal layer at a point in time for atmospheric chemical constituents
         {41,19,0, {1,1,2,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4,1,1,1} },
             // 4.42: Average, accumulation, and/or extreme values or other statistically-processed values
             // at a horizontal level or in a horizontal layer in a continuous or non-continuous
             // time interval for atmospheric chemical constituents
         {42,30,1, {1,1,2,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4,2,1,1,1,1,1,1,4,1,1,1,4,1,4} },
             // 4.43: Individual ensemble forecast, control and perturbed, at a horizontal level
             // or in a horizontal layer in a continuous or non-continuous
             // time interval for atmospheric chemical constituents
         {43,33,1, {1,1,2,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4,1,1,1,2,1,1,1,1,1,1,4,1,1,1,4,1,4} },
             // 4.254: CCITT IA5 Character String
         {254,3,0, {1,1,4} },
             // 4.1000: Cross section of analysis or forecast
             //         at a point in time
         {1000,9,0, {1,1,1,1,1,2,1,1,4} },
             // 4.1001: Cross section of Ave/Accum/etc... analysis or forecast
             //         in a time interval
         {1001,16,0, {1,1,1,1,1,2,1,1,4,4,1,1,1,4,1,4} },
             // 4.1001: Cross section of Ave/Accum/etc... analysis or forecast
             //         over latitude or longitude
         {1002,15,0, {1,1,1,1,1,2,1,1,4,1,1,1,4,4,2} },
             // 4.1100: Hovmoller-type grid w/ no averaging or other
             //         statistical processing
         {1100,15,0, {1,1,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4} },
             // 4.1100: Hovmoller-type grid with averaging or other
             //         statistical processing
         {1101,22,0, {1,1,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4,4,1,1,1,4,1,4} },
             // 4.32:Simulate (synthetic) Satellite Product
         {32,10,1, {1,1,1,1,1,2,1,1,2,1} },
             // 4.44: Analysis or forecast at a horizontal level or in a horizontal layer
             // at a point in time for Aerosol
         {44,21,0, {1,1,2,1,-1,-4,-1,-4,1,1,1,2,1,1,2,1,-1,-4,1,-1,-4} },
             // 4.45: Individual ensemble forecast, control and 
             // perturbed,  at a horizontal level or in a horizontal layer
             // at a point in time for Aerosol
         {45,24,0, {1,1,2,1,-1,-4,-1,-4,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4,1,1,1} },
             // 4.46: Ave or Accum or Extreme value at level/layer
             // at horizontal level or in a horizontal in a continuous or
             // non-continuous time interval for Aerosol
         {46,35,1, {1,1,2,1,-1,-4,-1,-4,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4,2,1,1,1,1,1,1,4,1,1,1,4,1,4} },
             // 4.47: Individual ensemble forecast, control and 
             // perturbed, at horizontal level or in a horizontal
             // in a continuous or non-continuous time interval for Aerosol
         {47,38,1, {1,1,1,2,1,-1,-4,-1,-4,1,1,2,1,1,4,1,-1,-4,1,-1,-4,1,1,1,2,1,1,1,1,1,1,4,1,1,1,4,1,4} },

             //             VALIDATION --- PDT 4.48
             // 4.48: Analysis or forecast at a horizontal level or in a horizontal layer
             // at a point in time for Optical Properties of Aerosol
         {48,26,0, {1,1,2,1,-1,-4,-1,-4,1,-1,-4,-1,-4,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4} },

             //             VALIDATION --- PDT 4.50
             // 4.50: Analysis or forecast of multi component parameter or
             // matrix element at a point in time
         {50,21,0, {1,1,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4,1,1,4,4,4,4} },

             //             VALIDATIONi --- PDT 4.52
             // 4.52: Analysis or forecast of Wave parameters
             // at the Sea surface at a point in time
         {52,15,0, {1,1,1,1,1,1,1,1,2,1,1,4,1,-1,-4} },

             // 4.51: Categorical forecasts at a horizontal level or
             // in a horizontal layer at a point in time
         {51,16,1, {1,1,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4,1} },
             // 4.91: Categorical forecasts at a horizontal level or
             // in a horizontal layer at a point in time
             // in a continuous or non-continuous time interval
         {91,16,1, {1,1,1,1,1,2,1,1,4,1,-1,-4,1,-1,-4,1} }

      } ;


#endif  /*  _pdstemplates_H  */
