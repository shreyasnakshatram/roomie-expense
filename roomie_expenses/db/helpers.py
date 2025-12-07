import os
import sqlite3

from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from db.models import engine, User, Expense


base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, "roomie_expenses.db")

Session = sessionmaker(bind=engine)
session = Session()


def bulk_add_expense_to_db(expenses_data: list) -> int:
    try:
        objs = [Expense(**rec) for rec in expenses_data]
        session.add_all(objs)
        session.commit()

        return len(objs)

    except SQLAlchemyError:
        session.rollback()

    finally:
        session.close()
    return 0

def add_expense_to_db(source: str, amount: float, added_by: int, month: str, year: int):
    new_expense = Expense(
        source_of_expense = source,
        amount = amount,
        added_by_id = added_by,
        month = month,
        year = year,
        created_at = datetime.utcnow(),
        updated_at = datetime.utcnow()
    )

    session.add(new_expense)
    session.commit()
    expense_id = new_expense.id
    session.close()
    return expense_id

def load_expenses_df():
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM expenses ORDER BY year DESC, month DESC, id DESC", conn)
    conn.close()
    if not df.empty:
        # human-friendly month name
        df["month_name"] = df["month"].apply(lambda m: datetime(1900, int(m), 1).strftime("%B"))
    return df


# ---------- User Helper Functions ----------
def get_all_user_names():
    user_query = (
        session.query(User).all()
    )

    users_list = []
    users_dict = {}
    for user in user_query:
        users_list.append(user.name)
        users_dict[user.name] = user.id 

    return users_list, users_dict
