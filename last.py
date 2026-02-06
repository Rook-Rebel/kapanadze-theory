import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- გვერდის კონფიგურაცია ---
st.set_page_config(
    page_title="Kapanadze Analytical Suite",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS დიზაინი ---
st.markdown("""
<style>
    h1 { margin-top: -50px; }
    .stAlert { font-size: 16px; }
    .math-box { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #2E86C1; }
    .core-message { 
        background-color: #ffeebb; 
        padding: 20px; 
        border-radius: 10px; 
        border: 2px solid #ffcc00; 
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: #333;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. მათემატიკური ძრავა (SymPy)
# ==========================================

def algebraic_derivative(func_str, x0):
    x, k = sp.symbols('x k')
    try:
        f = sp.sympify(func_str)
        f_x0 = f.subs(x, x0)
        
        # კაპანაძის განტოლება
        diff = f - (f_x0 + k * (x - x0))
        
        # ნაშთის გაშლა (ალგებრული ოპერაცია, ზღვრის გარეშე)
        series = sp.series(diff, x, x0, n=2).removeO()
        linear_term = series.coeff(x - x0)
        
        # ამოხსნა k-სთვის
        solution = sp.solve(linear_term, k)
        
        if not solution:
            return None, None, "ვერ მოიძებნა k"
            
        k_val = solution[0]
        tangent_eq = f_x0 + k_val * (x - x0)
        return f, k_val, tangent_eq
    except Exception as e:
        return None, None, str(e)

def solve_kapanadze_3d(func_str, x0_val, y0_val):
    x, y = sp.symbols('x y')
    kx, ky = sp.symbols('kx ky')
    try:
        func = sp.sympify(func_str)
        z0 = func.subs({x: x0_val, y: y0_val})
        kx_val = sp.diff(func, x).subs({x:x0_val, y:y0_val})
        ky_val = sp.diff(func, y).subs({x:x0_val, y:y0_val})
        return func, kx_val, ky_val, z0
    except Exception as e:
        return None, None, None, str(e)

# ==========================================
# 2. ინტერფეისი (ნავიგაცია)
# ==========================================

st.sidebar.markdown("# 📚 ნავიგაცია")
tab_selection = st.sidebar.radio("აირჩიეთ განყოფილება:", 
    ["I. გეომეტრიული არსი", 
     "II. ალგებრული კალკულატორი", 
     "III. ტოპოლოგია (3D)",
     "IV. ტრიგონომეტრია",
     "V. ლოგარითმული ანალიზი", 
     "VI. ფიზიკა (კინემატიკა)",
     "VII. განსაკუთრებული შემთხვევები"])

st.title("დავით კაპანაძის ალგებრული ანალიზის ლაბორატორია")

# --- მთავარი შეტყობინება (ზღვრის გარეშე) ---
st.markdown("""
<div class="core-message">
    ⚠️ მთავარი პრინციპი: ბატონი დავითის თეორია ითვლის წარმოებულს ზღვრების ($\lim$) გარეშე!
    <br><span style="font-size:16px; font-weight:normal">ჩვენ ვიყენებთ სუფთა ალგებრულ მეთოდს: ნაშთის კვადრატზე გაყოფას.</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------------------------------------------------------
# TAB 1: გეომეტრია
# -----------------------------------------------------------------------------
if tab_selection == "I. გეომეტრიული არსი":
    st.header("თავი I: როგორ იქცევა მკვეთი მხებად?")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.info("მხები არის მდგომარეობა, როდესაც ორი წერტილი ($A$ და $B$) ერთიანდება **ორჯერად ფესვად**.")
        func_input = st.text_input("ფუნქცია:", "x^2", key="geom_func")
        x_a = st.number_input("წერტილი A:", value=1.0, step=0.1)
        h = st.slider("წერტილი B-ს დაშორება (h):", 0.01, 2.0, 1.0, 0.01)
    with col2:
        x = sp.symbols('x')
        try:
            f = sp.sympify(func_input)
            f_lamb = sp.lambdify(x, f, 'numpy')
            xA, xB = x_a, x_a + h
            yA, yB = f_lamb(xA), f_lamb(xB)
            slope_secant = (yB - yA) / (xB - xA)
            slope_tangent = float(sp.diff(f, x).subs(x, xA))
            x_range = np.linspace(xA - 2, xB + 2, 500)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_range, y=f_lamb(x_range), name="f(x)", line=dict(color='#1f77b4', width=3)))
            fig.add_trace(go.Scatter(x=x_range, y=yA + slope_secant * (x_range - xA), name="მკვეთი", line=dict(color='#ff7f0e', dash='dash')))
            fig.add_trace(go.Scatter(x=x_range, y=yA + slope_tangent * (x_range - xA), name="მხები", line=dict(color='#2ca02c', width=2)))
            fig.add_trace(go.Scatter(x=[xA, xB], y=[yA, yB], mode='markers+text', text=["A", "B"], marker=dict(size=12, color=['black', 'red'])))
            fig.update_layout(title="ნახაზის ვიზუალიზაცია", height=500)
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e: st.error(e)

# -----------------------------------------------------------------------------
# TAB 2: ალგებრული კალკულატორი
# -----------------------------------------------------------------------------
elif tab_selection == "II. ალგებრული კალკულატორი":
    st.header("თავი II: ნაშთის კვადრატზე გაყოფის მეთოდი")
    
    st.warning("""
    **რევოლუციური მიდგომა:** ტრადიციული ანალიზისგან განსხვავებით, აქ **არ გამოიყენება ზღვრები ($\lim_{h \\to 0}$).**
    ჩვენ ვიყენებთ ნაშთის კვადრატზე გაყოფის პრინციპს, რაც წმინდა ალგებრული ოპერაციაა.
    """)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        f_in = st.text_input("ფუნქცია:", "sin(x) * exp(0.5*x)", key="alg_func")
        x0_in = st.number_input("x0:", value=1.0, step=0.1)
        calc_btn = st.button("გამოთვლა (Lim-ის გარეშე)", type="primary")
    if calc_btn:
        with col2:
            func_sym, k_res, tan_sym = algebraic_derivative(f_in, x0_in)
            if func_sym:
                st.latex(rf"f'(x) = {sp.latex(k_res)}")
                x_range = np.linspace(x0_in - 2, x0_in + 2, 600)
                f_lamb, t_lamb = sp.lambdify('x', func_sym, 'numpy'), sp.lambdify('x', tan_sym, 'numpy')
                y_f, y_t = f_lamb(x_range), t_lamb(x_range)
                with np.errstate(divide='ignore', invalid='ignore'): remainder = (y_f - y_t) / (x_range - x0_in)**2
                fig = make_subplots(rows=2, cols=1, subplot_titles=("ვიზუალური შეხება", "მტკიცებულება: ნაშთი / (x-x0)²"))
                fig.add_trace(go.Scatter(x=x_range, y=y_f, name="ფუნქცია", line=dict(color='#1f77b4')), row=1, col=1)
                fig.add_trace(go.Scatter(x=x_range, y=y_t, name="მხები", line=dict(color='#d62728', dash='dash')), row=1, col=1)
                fig.add_trace(go.Scatter(x=x_range, y=remainder, name="ნაშთი", line=dict(color='#2ca02c', width=2)), row=2, col=1)
                fig.update_layout(height=700)
                st.plotly_chart(fig, use_container_width=True)
                st.success("თუ მწვანე ხაზი უწყვეტია, თეორია დამტკიცდა!")
            else: st.error(f"შეცდომა: {tan_sym}")

# -----------------------------------------------------------------------------
# TAB 3: ტოპოლოგია (3D)
# -----------------------------------------------------------------------------
elif tab_selection == "III. ტოპოლოგია (3D)":
    st.header("თავი III: კაპანაძის თეორია სივრცეში")
    st.info("3D-ში ვეძებთ მხებ სიბრტყეს, რომელთანაც სხვაობა კვადრატული რიგის მცირეა.")
    col1, col2 = st.columns([1, 3])
    with col1:
        f3_str = st.text_input("z = f(x,y):", "x^2 + y^2 - 0.5*x*y")
        x0, y0 = st.number_input("x0:", 0.0), st.number_input("y0:", 0.0)
        btn_3d = st.button("აგება 3D", type="primary")
    if btn_3d:
        with col2:
            func_sym, kx, ky, z0 = solve_kapanadze_3d(f3_str, x0, y0)
            if func_sym:
                st.markdown(f"<div class='math-box'>ნაპოვნია: kx={float(kx):.2f}, ky={float(ky):.2f}</div>", unsafe_allow_html=True)
                x_v = np.linspace(x0-2, x0+2, 40)
                X, Y = np.meshgrid(x_v, x_v)
                x_sym, y_sym = sp.symbols('x y')
                Z = sp.lambdify((x_sym, y_sym), func_sym, 'numpy')(X, Y)
                Z_plane = float(z0) + float(kx)*(X-x0) + float(ky)*(Y-y0)
                fig = go.Figure()
                fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale='Viridis', opacity=0.8, name='Surface'))
                fig.add_trace(go.Surface(z=Z_plane, x=X, y=Y, colorscale=[[0,'red'],[1,'red']], opacity=0.5, showscale=False))
                fig.add_trace(go.Scatter3d(x=[x0], y=[y0], z=[float(z0)], mode='markers', marker=dict(size=10, color='black')))
                fig.update_layout(height=700)
                st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 4: ტრიგონომეტრია
# -----------------------------------------------------------------------------
elif tab_selection == "IV. ტრიგონომეტრია":
    st.header("თავი XII: ტრიგონომეტრიული ფუნქციები")
    st.info("სინუსის 'სიჩქარე' (წარმოებული) არის კოსინუსი. ეს ჩანს ერთეულოვან წრეწირზე მოძრაობისას.")
    col1, col2 = st.columns([1, 2])
    with col1:
        angle = st.slider("კუთხე (rad):", 0.0, 2*np.pi, 1.0, 0.1)
        st.markdown(f"**sin(t):** {np.sin(angle):.2f}")
        st.markdown(f"**cos(t):** {np.cos(angle):.2f} (დახრილობა)")
    with col2:
        t_vals = np.linspace(0, 2*np.pi, 100)
        circle_x, circle_y = np.cos(t_vals), np.sin(t_vals)
        P_x, P_y = np.cos(angle), np.sin(angle)
        tan_x = [P_x - 0.5*(-P_y), P_x + 0.5*(-P_y)]
        tan_y = [P_y - 0.5*(P_x), P_y + 0.5*(P_x)]
        fig = make_subplots(rows=1, cols=2, subplot_titles=("ერთეულოვანი წრეწირი", "y = sin(x)"))
        fig.add_trace(go.Scatter(x=circle_x, y=circle_y, line=dict(color='black')), row=1, col=1)
        fig.add_trace(go.Scatter(x=tan_x, y=tan_y, line=dict(color='red', width=3)), row=1, col=1)
        fig.add_trace(go.Scatter(x=[P_x], y=[P_y], mode='markers', marker=dict(color='blue')), row=1, col=1)
        fig.add_trace(go.Scatter(x=t_vals, y=np.sin(t_vals), line=dict(color='blue')), row=1, col=2)
        slope_x = np.linspace(angle-0.5, angle+0.5, 10)
        slope_y = np.sin(angle) + np.cos(angle)*(slope_x-angle)
        fig.add_trace(go.Scatter(x=slope_x, y=slope_y, line=dict(color='red', width=3)), row=1, col=2)
        fig.add_trace(go.Scatter(x=[angle], y=[np.sin(angle)], mode='markers', marker=dict(color='blue')), row=1, col=2)
        fig.update_layout(height=500, showlegend=False)
        fig.update_xaxes(scaleanchor="y", scaleratio=1, row=1, col=1)
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 5: ლოგარითმული ანალიზი
# -----------------------------------------------------------------------------
elif tab_selection == "V. ლოგარითმული ანალიზი":
    st.header("📈 ლოგარითმული ფუნქციები")
    st.info("კაპანაძის მეთოდით: $f(x) = \\log_a(x) \\Rightarrow f'(x) = \\frac{1}{x \\ln(a)}$")
    col1, col2 = st.columns([1, 2])
    with col1:
        base_type = st.selectbox("აირჩიეთ ფუძე:", ["e (ნატურალური ln)", "10 (ათობითი)", "2 (ორობითი)"])
        x0_log = st.number_input("წერტილი x0 (x > 0):", value=1.0, step=0.1, min_value=0.01)
        if "e" in base_type:
            log_func_str, display_str = "log(x)", "ln(x)"
        elif "10" in base_type:
            log_func_str, display_str = "log(x, 10)", "log_{10}(x)"
        else:
            log_func_str, display_str = "log(x, 2)", "log_{2}(x)"
        if st.button("გამოთვლა (Log)", type="primary"):
            func_sym, k_res, tan_sym = algebraic_derivative(log_func_str, x0_log)
            if func_sym:
                with col2:
                    st.latex(f"f'({x0_log}) = {sp.latex(k_res)}")
                    x_start = max(0.01, x0_log - 2)
                    x_range = np.linspace(x_start, x0_log + 2, 500)
                    f_lamb = sp.lambdify('x', func_sym, 'numpy')
                    t_lamb = sp.lambdify('x', tan_sym, 'numpy')
                    y_f, y_t = f_lamb(x_range), t_lamb(x_range)
                    with np.errstate(divide='ignore', invalid='ignore'): remainder = (y_f - y_t) / (x_range - x0_log)**2
                    fig = make_subplots(rows=2, cols=1, subplot_titles=(f"გრაფიკი: {display_str}", "ნაშთის ანალიზი"))
                    fig.add_trace(go.Scatter(x=x_range, y=y_f, name=display_str, line=dict(color='purple')), row=1, col=1)
                    fig.add_trace(go.Scatter(x=x_range, y=y_t, name="მხები", line=dict(color='orange', dash='dash')), row=1, col=1)
                    fig.add_trace(go.Scatter(x=[x0_log], y=[f_lamb(x0_log)], mode='markers', marker=dict(color='black', size=10), name='Point'), row=1, col=1)
                    fig.add_trace(go.Scatter(x=x_range, y=remainder, name="ნაშთი", line=dict(color='green')), row=2, col=1)
                    fig.update_layout(height=800)
                    st.plotly_chart(fig, use_container_width=True)
            else: st.error("შეცდომა გამოთვლისას.")

# -----------------------------------------------------------------------------
# TAB 6: ფიზიკა
# -----------------------------------------------------------------------------
elif tab_selection == "VI. ფიზიკა (კინემატიკა)":
    st.header("თავი XIII: ფიზიკური ინტერპრეტაცია")
    st.info("კაპანაძის მეთოდით, მხები არის ის წრფე, რომელსაც სხეული გაყვებოდა, მასზე მოქმედი ძალები რომ უცებ გამქრალიყო.")
    col1, col2 = st.columns([1, 2])
    with col1:
        t = st.slider("დრო (t):", 0.0, 2.0, 0.5, 0.05)
        x_val = t
        y_val = -(t**2) + 2
        vy = -2 * t
        st.markdown(f"**სიჩქარის ვექტორი:** (1, {vy:.2f})")
    with col2:
        t_range = np.linspace(0, 2, 100)
        x_traj = t_range
        y_traj = -(t_range**2) + 2
        slope = vy / 1
        x_tan = np.linspace(x_val, x_val + 0.5, 10)
        y_tan = y_val + slope * (x_tan - x_val)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_traj, y=y_traj, name="ტრაექტორია", line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=[x_val], y=[y_val], mode='markers', marker=dict(size=15, color='black'), name='სხეული'))
        fig.add_trace(go.Scatter(x=x_tan, y=y_tan, name="ინერცია", line=dict(color='red', width=3), mode='lines+markers', marker=dict(symbol='arrow', size=10)))
        fig.add_trace(go.Scatter(x=[0, 2], y=[-2, -2], line=dict(color='green', width=5), name='მიწა'))
        fig.update_layout(title="ბალისტიკური მოძრაობა", height=500, yaxis=dict(range=[-2.5, 2.5], scaleanchor="x", scaleratio=1))
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 7: განსაკუთრებული შემთხვევები
# -----------------------------------------------------------------------------
elif tab_selection == "VII. განსაკუთრებული შემთხვევები":
    st.header("🔬 თეორიის გამოყენების არეალი")
    st.info("აქ განხილულია ფუნქციები, სადაც 'ნაშთის კვადრატზე გაყოფის' მეთოდი სპეციფიკურ შედეგს იძლევა.")
    col1, col2 = st.columns([1, 2])
    with col1:
        problem_type = st.selectbox("ტიპი:", ["|x|^1.5 (ნაკლები სიგლუვე)", "x^2 * sin(1/x) (ოსცილაცია)"])
        if "1.5" in problem_type: st.markdown("ფუნქციას აქვს წარმოებული, მაგრამ ნაშთი არ მცირდება საკმარისად სწრაფად.")
        else: st.markdown("ფუნქცია ირხევა ძალიან სწრაფად, რის გამოც ნაშთი არ სტაბილურდება.")
    with col2:
        x = np.linspace(-0.5, 0.5, 1000)
        if "1.5" in problem_type:
            y = np.abs(x)**1.5
            tangent = np.zeros_like(x)
            with np.errstate(divide='ignore', invalid='ignore'): remainder = y / (x**2)
        else:
            y = (x**2) * np.sin(1/(x + 1e-9))
            tangent = np.zeros_like(x)
            with np.errstate(divide='ignore', invalid='ignore'): remainder = np.sin(1/(x + 1e-9))
        fig = make_subplots(rows=2, cols=1, subplot_titles=("ფუნქცია და მხები", "ნაშთის ანალიზი"))
        fig.add_trace(go.Scatter(x=x, y=y, name="ფუნქცია", line=dict(color='blue')), row=1, col=1)
        fig.add_trace(go.Scatter(x=x, y=tangent, name="მხები", line=dict(color='red', dash='dash')), row=1, col=1)
        fig.add_trace(go.Scatter(x=x, y=remainder, name="ნაშთი", line=dict(color='purple')), row=2, col=1)
        fig.update_layout(height=600)
        if "ოსცილაცია" in problem_type: fig.update_yaxes(range=[-2, 2], row=2, col=1)
        else: fig.update_yaxes(range=[0, 20], row=2, col=1)
        st.plotly_chart(fig, use_container_width=True)
        st.info("დასკვნა: ამ კონკრეტულ შემთხვევაში მეთოდი პირდაპირ არ გამოიყენება, რადგან ნაშთი არ აკმაყოფილებს კაპანაძის პირობას.")