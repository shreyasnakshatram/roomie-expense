# seed_users.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User   # <-- Make sure this path matches your project structure
import os

# --------- DB Setup ----------
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, "roomie_expenses.db")

engine = create_engine(f"sqlite:///{db_path}", echo=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# --------- Migration Data ----------
default_users = [
    {"name": "Varun", "email": None},
    {"name": "Shashank", "email": None},
    {"name": "Charan", "email": None},
    {"name": "Aravind", "email": None},
    {"name": "Swapnik", "email": None},
]

# --------- Insert Logic ----------
def seed_users():
    for u in default_users:
        existing = session.query(User).filter_by(name=u["name"]).first()
        if not existing:
            new_user = User(
                name=u["name"],
                email=u["email"],
                password=None  # ignoring password as you asked
            )
            session.add(new_user)
            print(f"Added user → {u['name']}")
        else:
            print(f"User {u['name']} already exists → skipping")

    session.commit()
    print("\nUser seeding completed!")

# --------- Run Migration ----------
if __name__ == "__main__":
    # Ensure tables exist
    Base.metadata.create_all(engine)

    seed_users()

# # ====== Pagination controls (drop in before rendering cards) ======
# import math
# import streamlit as st

# # read current query params (new API)
# params = st.query_params

# # page size options and defaults
# page_size_options = [5, 10, 20, 50]
# default_page_size = 10

# # read page and page_size from URL query params (fallback to defaults)
# try:
#     page = int(params.get("page", [1])[0])
#     if page < 1:
#         page = 1
# except Exception:
#     page = 1

# try:
#     page_size = int(params.get("page_size", [default_page_size])[0])
#     if page_size not in page_size_options:
#         page_size = default_page_size
# except Exception:
#     page_size = default_page_size

# # ensure filtered (the DF you prepared earlier) is available
# total_items = len(filtered)
# total_pages = max(1, math.ceil(total_items / page_size))

# # clamp page to valid range
# if page > total_pages:
#     page = total_pages

# # UI: pagination controls (compact)
# with st.container():
#     c1, c2, c3, c4 = st.columns([1, 2, 3, 2])
#     with c1:
#         # page size selector
#         new_page_size = st.selectbox("Page size", page_size_options, index=page_size_options.index(page_size), key="page_size_select")
#         if new_page_size != page_size:
#             # update URL param (reset to page 1)
#             st.query_params["page_size"] = str(new_page_size)
#             st.query_params["page"] = "1"
#             st.experimental_rerun()
#     with c2:
#         # Previous / Next buttons
#         prev_clicked = st.button("◀ Prev", disabled=(page <= 1), key="pag_prev")
#         next_clicked = st.button("Next ▶", disabled=(page >= total_pages), key="pag_next")
#         if prev_clicked:
#             st.query_params["page"] = str(max(1, page - 1))
#             st.experimental_rerun()
#         if next_clicked:
#             st.query_params["page"] = str(min(total_pages, page + 1))
#             st.experimental_rerun()
#     with c3:
#         # direct page jump
#         st.markdown(f"**Page {page} of {total_pages}**  &nbsp;&nbsp; — &nbsp;&nbsp; {total_items} items")
#     with c4:
#         # quick goto input
#         goto = st.text_input("Go to page", value=str(page), key="goto_page_input")
#         try:
#             goto_int = int(goto)
#             if goto_int != page and 1 <= goto_int <= total_pages:
#                 st.query_params["page"] = str(goto_int)
#                 st.experimental_rerun()
#         except Exception:
#             # ignore non-int input until user fixes it
#             pass

# # compute slice indices and show a small hint
# start_idx = (page - 1) * page_size
# end_idx = start_idx + page_size
# # make a page-sliced frame to render below
# filtered_sorted = filtered.sort_values("created_at", ascending=False).reset_index(drop=True)
# filtered_page = filtered_sorted.iloc[start_idx:end_idx]

# # optionally show which items are displayed (small debug)
# st.markdown(f"Showing items **{start_idx + 1}** – **{min(end_idx, total_items)}** of **{total_items}**")

# # Use `filtered_page` in place of `filtered` for the rendering loop that follows
# # e.g. replace: `for _, row in filtered.sort_values(...).iterrows():`
# # with:     `for _, row in filtered_page.iterrows():`

# # IMPORTANT: if edit_expense is set and the edited item is not on the current page,
# # keep the current page but allow editing by loading the full row if needed:
# editing = params.get("edit_expense", [None])[0]
# if editing:
#     try:
#         editing_id = int(editing)
#     except Exception:
#         editing_id = None
# else:
#     editing_id = None

# # If editing a row that's not on current page, optionally fetch that row and show it
# if editing_id is not None and editing_id not in filtered_page["id"].tolist():
#     # find the editing row in the full filtered set (so user sees the edit form even if item is off-page)
#     edit_row = filtered_sorted[filtered_sorted["id"] == editing_id]
#     if not edit_row.empty:
#         # render the single editing card above the paginated list (reuse your card rendering logic)
#         single = edit_row.iloc[0:1]
#         # you can render it (or set filtered_page = pd.concat([single, filtered_page])).
#         # For simplicity, put the editing row at the top of the paginated list:
#         filtered_page = pd.concat([single, filtered_page]).reset_index(drop=True)

# # From here on, use `filtered_page` in your existing card rendering loop.
# # Example replacement comment:
# #   for _, row in filtered_page.iterrows():
# #       ... render card ...
# # ====== end pagination block ======
