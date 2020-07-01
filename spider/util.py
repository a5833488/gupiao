from plotly.utils import lock


def sql_process(db,cursor,sql):
    lock.acquire()
    try:
        cursor.execute(sql)
        db.commit()
        print(sql)
    except Exception as  e:
        # 如果发生错误则回滚
        db.rollback()
        cursor.close()
        print("更新失败"+e)
    finally:
        lock.release()