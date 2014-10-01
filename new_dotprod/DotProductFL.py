#=========================================================================
# MatrixVecFL
#=========================================================================

import greenlet

from new_pymtl import *
from new_pmlib import *
from MatrixVec import MatrixVec

import numpy

from pmlib_extra import GreenletWrapper,BytesMemPortProxy
from new_pmlib.queues import ChildReqRespQueueAdapter
from pmlib_extra import ListMemPortAdapter

class DotProduct (Model):

  def __init__( s, mem_ifc_types, cpu_ifc_types ):
    s.cpu_ifc = ChildReqRespBundle ( cpu_ifc_types )
    s.mem_ifc = ParentReqRespBundle( mem_ifc_types )

    s.cpu      = ChildReqRespQueueAdapter( s.cpu_ifc )
    # s.mem      = BytesMemPortProxy( s.mem_ifc )
    # s.xcel_dot = MatrixVec( s.mem )

    s.src0 = ListMemPortAdapter( s.mem_ifc, s )
    s.src1 = ListMemPortAdapter( s.mem_ifc, s )

    @s.tick_fl
    def logic():
      s.cpu.xtick()
      if not s.cpu.req_q.empty() and not s.cpu.resp_q.full():
        req = s.cpu.get_req()
        if   req.creg == 1: s.size = req.data
        elif req.creg == 2: s.src0.set_base( req.data )
        elif req.creg == 3: s.src1.set_base( req.data )
        print s.src0.is_rdy()
        if s.src0.is_rdy() and s.src1.is_rdy():
          result = numpy.dot( s.src0, s.src1 )
          s.cpu.push_resp( result )

  #-----------------------------------------------------------------------
  # line_trace
  #-----------------------------------------------------------------------

  def line_trace( s ):
    return "(" + str(s.cpu.req_q.empty()) + ")"

  def elaborate_logic( s ):
    pass
