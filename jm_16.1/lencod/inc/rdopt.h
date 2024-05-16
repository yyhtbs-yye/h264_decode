/*!
 ***************************************************************************
 * \file
 *    rdopt.h
 *
 * \author
 *    Alexis Michael Tourapis
 *
 * \date
 *    2 January 2008
 *
 * \brief
 *    Headerfile for RDO
 **************************************************************************
 */

#ifndef _RDO_H_
#define _RDO_H_

#include "global.h"
#include "rdopt_coding_state.h"

// Motion Vector structure
typedef struct
{
  double rdcost;
  double dcost;
  double rate;   // why is rate a double? Could we use int64 or even simply int given that this is for a MB? Could a MB require int64 bits (answer is no)? 
  int   cbp;
  distblk  cost;
  short c_imode;
  short i16offset;
  byte  mode;
} BestMode;

struct rdo_structure
{
  RD_8x8DATA *tr4x4;
  RD_8x8DATA *tr8x8;
  imgpel ***rec8x8;
  imgpel ***rec4x4;
  imgpel **pred;
  imgpel ***rec_mb;
  int    **lrec_rec;
  int   ***lrec_rec_uv;

  int   ****cofAC;
  int    ***cofDC; 
  int     **cofAC4x4;
  int   ****cofAC4x4intern;

  short *****all_mv8x8; 

  int   *****cofAC4x4CbCrintern;
  int   *****cofAC8x8ts;        // [plane][8x8block][4x4block][level/run][scan_pos]
  int   *****coefAC8x8;
  int   *****coefAC8x8intra;
  int   **cofAC4x4CbCr[2];


  int   cbp;
  char  **l0_refframe;
  char  **l1_refframe;

  Info8x8 best8x8[4];

  CSobj *cs_mb;
  CSobj *cs_b8;
  CSobj *cs_cm;
  CSobj *cs_tmp;

  BestMode mode_best;

// adaptive langrangian parameters
  double lambda_mf_factor;
};


extern int  GetBestTransformP8x8 (Macroblock *currMB);
extern byte field_flag_inference (Macroblock  *currMB);
extern distblk rdcost_for_4x4_intra_blocks     (Macroblock *currMB, int* nonzero, int b8, int b4, int ipmode, int lambda, int mostProbableMode, distblk min_rdcost);
extern distblk rdcost_for_4x4_intra_blocks_444 (Macroblock *currMB, int* nonzero, int b8, int b4, int ipmode, int lambda, int mostProbableMode, distblk min_rdcost);
extern int valid_intra_mode(Slice *currSlice, int ipmode);

extern void init_md_best(BestMode  *best);

extern void generate_pred_error_4x4(imgpel **cur_img, imgpel **prd_img, imgpel **cur_prd, 
                         int **mb_rres, int pic_opix_x, int block_x);
extern void generate_pred_error_8x8(imgpel **cur_img, imgpel **prd_img, imgpel **cur_prd, 
                         int **mb_rres, int pic_opix_x, int block_x);

//============= rate-distortion optimization ===================
extern void  clear_rdopt (Slice *currSlice);
extern void  init_rdopt  (Slice *currSlice);

extern void UpdatePixelMap(VideoParameters *p_Vid, InputParameters *p_Inp);

extern void   update_qp_cbp     (Macroblock *currMB);
extern void   update_qp_cbp_tmp (Macroblock *currMB, int cbp);

extern void alloc_rd8x8data (RD_8x8DATA *rd_data);
extern void free_rd8x8data  (RD_8x8DATA *rd_data);

extern void restore_nz_coeff(Macroblock *currMB);

extern void end_encode_one_macroblock(Macroblock *currMB);

extern void encode_one_macroblock_low          (Macroblock *currMB);
extern void encode_one_macroblock_high         (Macroblock *currMB);
extern void encode_one_macroblock_highfast     (Macroblock *currMB);
extern void encode_one_macroblock_highloss     (Macroblock *currMB);

extern void store_8x8_motion_vectors_p_slice(Slice *currSlice, int dir, int block8x8, Info8x8 *B8x8Info);
extern void store_8x8_motion_vectors_b_slice(Slice *currSlice, int dir, int block8x8, Info8x8 *B8x8Info);


/*!
 *************************************************************************************
 * \brief
 *    copy data in iblock to oblock
 *************************************************************************************
 */
static inline void copy_4x4block(imgpel **oblock, imgpel **iblock, int o_xoffset, int i_xoffset)
{
  int y;
  for (y = 0; y < BLOCK_SIZE; y++)
  {
    memcpy(&oblock[y][o_xoffset],&iblock[y][i_xoffset], BLOCK_SIZE * sizeof(imgpel));
  }
}
#endif

