"""
初始化测试数据
"""

from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.database.models import User, Order, Track


def seed_database():
    db: Session = SessionLocal()

    try:
        if db.query(User).first():
            print("数据库已有数据，跳过初始化。")
            return

        user = User(
            name="张三",
            phone="13800138000",
            email="zhangsan@test.com"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print("✅ user ok")

        order1 = Order(
            order_no="SF123456",
            sender="深圳华强北",
            receiver="北京市朝阳区",
            status="运输中",
            city="杭州转运中心",
            eta="2026-07-01",
            user_id=user.id
        )

        db.add(order1)
        db.commit()
        db.refresh(order1)
        print("✅ order1 ok")

        order2 = Order(
            order_no="SF888888",
            sender="上海浦东新区",
            receiver="广州市天河区",
            status="已签收",
            city="广州",
            eta="2026-06-28",
            user_id=user.id
        )

        db.add(order2)
        db.commit()
        db.refresh(order2)
        print("✅ order2 ok")

        # ======================
        # 创建物流轨迹
        # ======================

        tracks = [

            Track(
                order_id=order1.id,
                city="深圳",
                remark="包裹已揽收",
                track_time="2026-06-28 09:00"
            ),

            Track(
                order_id=order1.id,
                city="广州",
                remark="到达广州转运中心",
                track_time="2026-06-28 18:00"
            ),

            Track(
                order_id=order1.id,
                city="杭州",
                remark="到达杭州转运中心",
                track_time="2026-06-29 08:30"
            ),

            Track(
                order_id=order1.id,
                city="杭州",
                remark="等待派送",
                track_time="2026-06-29 12:00"
            ),

            Track(
                order_id=order2.id,
                city="上海",
                remark="包裹已揽收",
                track_time="2026-06-26 10:00"
            ),

            Track(
                order_id=order2.id,
                city="广州",
                remark="已签收",
                track_time="2026-06-28 15:30"
            ),
        ]

        db.add_all(tracks)
        db.commit()
        print("✅ tracks ok")

    except Exception as e:
        db.rollback()
        print("❌ seed失败：", e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()