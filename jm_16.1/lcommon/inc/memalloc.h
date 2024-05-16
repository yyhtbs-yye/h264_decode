
/*!
 ************************************************************************
 * \file  memalloc.h
 *
 * \brief
 *    Memory allocation and free helper funtions
 *
 * \author
 *    Main contributors (see contributors.h for copyright, address and affiliation details)
 *     - Karsten S�hring                 <suehring@hhi.de> 
 *     - Alexis Michael Tourapis         <alexismt@ieee.org> 
 *
 ************************************************************************
 */

#ifndef _MEMALLOC_H_
#define _MEMALLOC_H_

#include "global.h"
#include "distortion.h"
#include "lagrangian.h"
#include "quant_params.h"

#if defined(USEMMX) // && (IMGTYPE == 0) // MMX, SSE, SSE2 intrinsic support
#if defined(_MSC_VER) || defined(__INTEL_COMPILER) // ICC
#  include <emmintrin.h>
# else
#  include <xmmintrin.h>
# endif
#endif

extern int  get_mem2Ddist(DistortionData ***array2D, int dim0, int dim1);

extern int  get_mem2Dlm  (LambdaParams ***array2D, int dim0, int dim1);
extern int  get_mem2Dolm (LambdaParams ***array2D, int dim0, int dim1, int offset);

extern int  get_mem2Dmp  (PicMotionParams2 ***array2D, int dim0, int dim1);
extern int  get_mem3Dmp  (PicMotionParams2 ****array3D, int dim0, int dim1, int dim2);

extern int  get_mem2Dquant(LevelQuantParams ***array2D, int dim0, int dim1);
extern int  get_mem3Dquant(LevelQuantParams ****array3D, int dim0, int dim1, int dim2);
extern int  get_mem4Dquant(LevelQuantParams *****array4D, int dim0, int dim1, int dim2, int dim3);
extern int  get_mem5Dquant(LevelQuantParams ******array5D, int dim0, int dim1, int dim2, int dim3, int dim4);

extern int  get_mem2Dmv  (MotionVector ***array2D, int dim0, int dim1);
extern int  get_mem3Dmv  (MotionVector ****array3D, int dim0, int dim1, int dim2);
extern int  get_mem4Dmv  (MotionVector *****array4D, int dim0, int dim1, int dim2, int dim3);
extern int  get_mem5Dmv  (MotionVector ******array5D, int dim0, int dim1, int dim2, int dim3, int dim4);

extern int  get_mem2D(byte ***array2D, int dim0, int dim1);
extern int  get_mem3D(byte ****array3D, int dim0, int dim1, int dim2);
extern int  get_mem4D(byte *****array4D, int dim0, int dim1, int dim2, int dim3);

extern int  get_mem2Dint(int ***array2D, int rows, int columns);
extern int  get_mem2Dint64(int64 ***array2D, int rows, int columns);
extern int  get_mem3Dint(int ****array3D, int frames, int rows, int columns);
extern int  get_mem3Dint64(int64 ****array3D, int frames, int rows, int columns);
extern int  get_mem4Dint(int *****array4D, int idx, int frames, int rows, int columns );
extern int  get_mem4Dint64(int64 *****array4D, int idx, int frames, int rows, int columns );
extern int  get_mem5Dint(int ******array5D, int refs, int blocktype, int rows, int columns, int component);


extern int get_mem3Duint16(uint16 ****array3D,int dim0, int dim1, int dim2);

extern int  get_mem2Ddistblk(distblk ***array2D, int rows, int columns);
extern int  get_mem3Ddistblk(distblk ****array3D, int frames, int rows, int columns);
extern int  get_mem4Ddistblk(distblk *****array4D, int idx, int frames, int rows, int columns );

extern int  get_mem2Dshort(short ***array2D, int dim0, int dim1);
extern int  get_mem3Dshort(short ****array3D, int dim0, int dim1, int dim2);
extern int  get_mem4Dshort(short *****array4D, int dim0, int dim1, int dim2, int dim3);
extern int  get_mem5Dshort(short ******array5D, int dim0, int dim1, int dim2, int dim3, int dim4);
extern int  get_mem6Dshort(short *******array6D, int dim0, int dim1, int dim2, int dim3, int dim4, int dim5);
extern int  get_mem7Dshort(short ********array7D, int dim0, int dim1, int dim2, int dim3, int dim4, int dim5, int dim6);

extern int  get_mem1Dpel(imgpel **array2D, int rows);
extern int  get_mem2Dpel(imgpel ***array2D, int rows, int columns);
extern int  get_mem3Dpel(imgpel ****array3D, int frames, int rows, int columns);
extern int  get_mem4Dpel(imgpel *****array4D, int sub_x, int sub_y, int rows, int columns);
extern int  get_mem5Dpel(imgpel ******array5D, int dims, int sub_x, int sub_y, int rows, int columns);

extern int  get_mem2Ddouble (double ***array2D, int rows, int columns);
extern int  get_mem2Dodouble(double ***array2D, int rows, int columns, int offset);
extern int  get_mem3Dodouble(double ****array2D, int rows, int columns, int pels, int offset);

extern int  get_mem2Doint (int ***array2D, int rows, int columns, int offset);
extern int  get_mem3Doint (int ****array3D, int rows, int columns, int pels, int offset);

extern int  get_offset_mem2Dshort(short ***array2D, int rows, int columns, int offset_y, int offset_x);

extern void free_offset_mem2Dshort(short **array2D, int columns, int offset_x, int offset_y);

extern void free_mem2Ddist (DistortionData **array2D);

extern void free_mem2Dlm   (LambdaParams **array2D);
extern void free_mem2Dolm  (LambdaParams **array2D, int offset);

extern void free_mem2Dmp   (PicMotionParams2    **array2D);
extern void free_mem3Dmp   (PicMotionParams2   ***array2D);

extern void free_mem2Dquant(LevelQuantParams    **array2D);
extern void free_mem3Dquant(LevelQuantParams   ***array2D);
extern void free_mem4Dquant(LevelQuantParams  ****array2D);
extern void free_mem5Dquant(LevelQuantParams *****array2D);

extern void free_mem2Dmv   (MotionVector    **array2D);
extern void free_mem3Dmv   (MotionVector   ***array2D);
extern void free_mem4Dmv   (MotionVector  ****array2D);
extern void free_mem5Dmv   (MotionVector *****array2D);

extern void free_mem2D     (byte      **array2D);
extern void free_mem3D     (byte     ***array3D);
extern void free_mem4D     (byte    ****array4D);

extern void free_mem2Dint  (int       **array2D);
extern void free_mem3Dint  (int      ***array3D);
extern void free_mem4Dint  (int     ****array4D);
extern void free_mem5Dint  (int    *****array5D);

extern void free_mem2Dint64(int64     **array2D);
extern void free_mem3Dint64(int64    ***array3D);
extern void free_mem4Dint64(int64     ****array4D);

extern void free_mem2Ddistblk(distblk     **array2D);
extern void free_mem3Ddistblk(distblk    ***array3D);
extern void free_mem4Ddistblk(distblk     ****array4D);

extern void free_mem2Dshort(short      **array2D);
extern void free_mem3Dshort(short     ***array3D);
extern void free_mem4Dshort(short    ****array4D);
extern void free_mem5Dshort(short   *****array5D);
extern void free_mem6Dshort(short  ******array6D);
extern void free_mem7Dshort(short *******array7D);

extern void free_mem1Dpel  (imgpel     *array1D);
extern void free_mem2Dpel  (imgpel    **array2D);
extern void free_mem3Dpel  (imgpel   ***array3D);
extern void free_mem4Dpel  (imgpel  ****array4D);
extern void free_mem5Dpel  (imgpel *****array5D);
extern void free_mem2Ddouble(double **array2D);
extern void free_mem3Ddouble(double ***array3D);

extern void free_mem2Dodouble(double **array2D, int offset);
extern void free_mem3Dodouble(double ***array3D, int rows, int columns, int offset);
extern void free_mem2Doint   (int **array2D, int offset);
extern void free_mem3Doint   (int ***array3D, int rows, int columns, int offset);

extern int init_top_bot_planes(imgpel **imgFrame, int height, imgpel ***imgTopField, imgpel ***imgBotField);
extern void free_top_bot_planes(imgpel **imgTopField, imgpel **imgBotField);

extern void no_mem_exit(char *where);

#endif
