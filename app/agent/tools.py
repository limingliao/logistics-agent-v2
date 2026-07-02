"""
tools.py

LLM Tool 定义
"""

from app.services.order_service import OrderService


# =====================================================
# Tool 实现
# =====================================================

class LogisticsTools:

    @staticmethod
    def query_order(db, order_no):
        """
        查询订单
        """

        result = OrderService.get_order_detail(
            db=db,
            order_no=order_no
        )

        if not result:
            return {
                "success": False,
                "message": "订单不存在"
            }

        order = result["order"]
        tracks = result["tracks"]

        return {
            "success": True,
            "order_no": order.order_no,
            "status": order.status,
            "city": order.city,
            "eta": str(order.eta),
            "tracks": [
                {
                    "time": str(track.track_time),
                    "city": track.city,
                    "remark": track.remark
                }
                for track in tracks
            ]
        }