CARD_CSS = """
<style>
.user-card {
  background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  border-radius: 12px;
  padding: 14px;
  box-shadow: 0 4px 14px rgba(2,6,23,0.6);
  border: 1px solid rgba(255,255,255,0.03);
  transition: transform .08s ease-in-out;
}
.user-card:hover { transform: translateY(-4px); }
.user-avatar {
  width: 48px; height: 48px; border-radius: 10px;
  display:inline-block; text-align:center; line-height:48px; font-weight:700;
  background: linear-gradient(135deg,#3b82f6,#7c3aed); color:white;
}
.user-name { font-size: 16px; font-weight: 700; margin: 0; }
.user-meta { color: rgba(255,255,255,0.7); margin: 0; font-size: 13px; }
.view-button { margin-top:8px; }
</style>
"""

