import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ==================== 參數設定 ====================
freq = 50                    # 50 Hz
amp = 230 / np.sqrt(2)      # 相電壓振幅 (RMS 230V)
t = np.linspace(0, 0.1, 5000)  # 0 ~ 0.1 秒 (5 個週期)

# ==================== 計算三相電壓 ====================
# 相電壓 (Phase voltage)
phase_a = amp * np.sin(2 * np.pi * freq * t)
phase_b = amp * np.sin(2 * np.pi * freq * t - 2 * np.pi / 3)
phase_c = amp * np.sin(2 * np.pi * freq * t + 2 * np.pi / 3)

# 線電壓 (Line voltage): U_AB = V_A - V_B
line_ab = phase_a - phase_b
line_bc = phase_b - phase_c
line_ca = phase_c - phase_a

# 計算 RMS 值
rms_phase = amp / np.sqrt(2)
rms_line = rms_phase * np.sqrt(3)

# ==================== 繪製圖表 ====================
fig = plt.figure(figsize=(16, 10))

# ========== 上方：相電壓 (Phase Voltage) ==========
ax1 = plt.subplot(2, 1, 1)
ax1.plot(t * 1000, phase_a, label='Phase A', color='#FF0000', linewidth=2.5, linestyle='-')
ax1.plot(t * 1000, phase_b, label='Phase B', color='#00AA00', linewidth=2.5, linestyle='-')
ax1.plot(t * 1000, phase_c, label='Phase C', color='#0000FF', linewidth=2.5, linestyle='-')

# 標註相位差 (120°)
idx_phase = len(t) // 10
ax1.annotate('', xy=(t[idx_phase+400]*1000, phase_b[idx_phase+400]), 
             xytext=(t[idx_phase]*1000, phase_a[idx_phase]),
             arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
ax1.text((t[idx_phase]+t[idx_phase+400])/2*1000, 250, '120°', fontsize=10, 
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

ax1.set_title('Phase Voltage (相電壓)', fontsize=14, fontweight='bold')
ax1.set_xlabel('Time (ms)', fontsize=11)
ax1.set_ylabel('Voltage (V)', fontsize=11)
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend(loc='upper right', fontsize=11)
ax1.set_xlim(0, 100)

# 標註 RMS 值
textstr = f'RMS (相電壓): {rms_phase:.1f} V\nPhase Sequence: A → B → C'
ax1.text(0.02, 0.95, textstr, transform=ax1.transAxes, fontsize=11,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

# ========== 下方：線電壓 (Line Voltage) ==========
ax2 = plt.subplot(2, 1, 2)
ax2.plot(t * 1000, line_ab, label='Line U_AB (A-B)', color='#FF0000', linewidth=2.5, linestyle='-')
ax2.plot(t * 1000, line_bc, label='Line U_BC (B-C)', color='#00AA00', linewidth=2.5, linestyle='-')
ax2.plot(t * 1000, line_ca, label='Line U_CA (C-A)', color='#0000FF', linewidth=2.5, linestyle='-')

ax2.set_title('Line Voltage (線電壓) = Phase A - Phase B', fontsize=14, fontweight='bold')
ax2.set_xlabel('Time (ms)', fontsize=11)
ax2.set_ylabel('Voltage (V)', fontsize=11)
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend(loc='upper right', fontsize=11)
ax2.set_xlim(0, 100)

# 標註 RMS 值
textstr_line = f'RMS (線電壓): {rms_line:.1f} V\nLine/Phase Ratio: √3 ≈ 1.732'
ax2.text(0.02, 0.95, textstr_line, transform=ax2.transAxes, fontsize=11,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.savefig('three_phase_waveform.png', dpi=300, bbox_inches='tight')
print("✓ 圖表已保存為: three_phase_waveform.png")
plt.show()

# ==================== 相位圖 (Phasor Diagram) ====================
fig2, ax3 = plt.subplots(figsize=(10, 10))

# 三相相位向量 (起始時刻 t=0)
angle_a = 0
angle_b = -2 * np.pi / 3  # -120°
angle_c = 2 * np.pi / 3   # 120°

# 繪製相位向量
ax3.arrow(0, 0, rms_phase * np.cos(angle_a), rms_phase * np.sin(angle_a), 
          head_width=20, head_length=15, fc='#FF0000', ec='#FF0000', linewidth=2.5, label='Phase A')
ax3.arrow(0, 0, rms_phase * np.cos(angle_b), rms_phase * np.sin(angle_b), 
          head_width=20, head_length=15, fc='#00AA00', ec='#00AA00', linewidth=2.5, label='Phase B')
ax3.arrow(0, 0, rms_phase * np.cos(angle_c), rms_phase * np.sin(angle_c), 
          head_width=20, head_length=15, fc='#0000FF', ec='#0000FF', linewidth=2.5, label='Phase C')

# 繪製線電壓向量
ax3.arrow(0, 0, rms_line * np.cos(angle_a + np.pi/6), rms_line * np.sin(angle_a + np.pi/6),
          head_width=25, head_length=20, fc='red', ec='red', linewidth=2, linestyle='--', alpha=0.6, label='Line U_AB')

# 設定圖表
ax3.set_xlim(-450, 450)
ax3.set_ylim(-450, 450)
ax3.set_aspect('equal')
ax3.grid(True, linestyle='--', alpha=0.5)
ax3.axhline(y=0, color='k', linewidth=0.5)
ax3.axvline(x=0, color='k', linewidth=0.5)

# 標籤和標題
ax3.set_xlabel('Real Axis', fontsize=12)
ax3.set_ylabel('Imaginary Axis', fontsize=12)
ax3.set_title('Three-Phase Phasor Diagram (相位圖)', fontsize=14, fontweight='bold')
ax3.legend(loc='upper right', fontsize=11)

# 標註角度
ax3.text(150, 50, '0°', fontsize=11, color='#FF0000', fontweight='bold')
ax3.text(-180, -100, '-120° (240°)', fontsize=11, color='#00AA00', fontweight='bold')
ax3.text(-100, 180, '+120°', fontsize=11, color='#0000FF', fontweight='bold')

# 標註資訊
info_text = f'Phase Voltage RMS: {rms_phase:.1f} V\nLine Voltage RMS: {rms_line:.1f} V\nFrequency: {freq} Hz\nPhase Sequence: A → B → C (Positive)'
ax3.text(0.02, 0.98, info_text, transform=ax3.transAxes, fontsize=11,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

plt.tight_layout()
plt.savefig('phasor_diagram.png', dpi=300, bbox_inches='tight')
print("✓ 相位圖已保存為: phasor_diagram.png")
plt.show()

# ==================== 列印計算結果 ====================
print("\n" + "="*60)
print("三相交流電 (Three-Phase AC) 計算結果")
print("="*60)
print(f"頻率 (Frequency):        {freq} Hz")
print(f"相電壓 RMS:              {rms_phase:.2f} V")
print(f"線電壓 RMS:              {rms_line:.2f} V")
print(f"線電壓/相電壓:           √3 = {np.sqrt(3):.3f}")
print(f"相位差:                 120° (或 2π/3 弧度)")
print(f"相序 (Phase Sequence):   A → B → C (正序)")
print("="*60 + "\n")
