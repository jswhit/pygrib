#ifndef _PYGRIB_PORTABLE_H_
#define _PYGRIB_PORTABLE_H_

#ifdef _WIN32

#include <io.h>
#define wrap_dup _dup

#else

#include <unistd.h>
#define wrap_dup dup

#endif  /* _WIN32 */

#endif  /* _PYGRIB_PORTABLE_H_ */
