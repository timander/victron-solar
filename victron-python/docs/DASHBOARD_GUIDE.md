# Solar Dashboard Guide: Understanding Your Victron MPPT Data

## Quick Start

Generate your comprehensive dashboard:
```bash
cd victron-python
make dashboard CSV=../data/SolarHistory.csv
```

This creates `solar_dashboard.png` - a professional 8-panel visualization of your solar system performance.

---

## Dashboard Panels Explained

### Panel 1: Daily Solar Energy Production (Top Left)
**What it shows:** Bar chart of daily energy yield in Wh  
**Red dashed line:** Your average daily production

**Key Insights:**
- **Consistent bars** = Stable solar generation
- **Low bars** = Cloudy days or system issues
- **Bars above average** = Good solar conditions
- **Very low/zero yields** = Possible panel shading or malfunction

**What to look for:**
- Days below 50% of average may indicate problems
- Increasing trend = Improving weather or fixing issues
- Decreasing trend = Deteriorating conditions or panel degradation

---

### Panel 2: System Summary (Top Right)
**What it shows:** Key statistics and health indicators

**Metrics Explained:**
- **Total Energy:** Cumulative production over the period
- **Daily Average:** What to expect on a typical day
- **Peak Power:** Maximum instantaneous power your panels have produced
- **Max Voltage:** Highest battery charge level reached
- **Min Voltage:** Lowest battery discharge level

**Battery Health Indicators:**
| Min Voltage | Status | Meaning |
|-------------|--------|---------|
| > 12.6V | ✅ Excellent | Battery stays well-charged |
| 12.2-12.6V | ⚠️ Fair | Moderate discharge cycles |
| < 12.2V | ❌ Concerning | Deep discharge, may reduce battery life |

**Warnings to watch:**
- "Battery may be undercharged" = Solar array may be too small for your usage
- "Battery may be oversized" = Your solar can't fully charge battery capacity

---

### Panel 3: Battery Voltage Behavior (Middle Left)
**What it shows:** Daily min/max battery voltages with reference lines

**Reference Voltages (12V system):**
- **14.4V (Blue):** Absorption setpoint - where bulk charging stops
- **13.5V (Orange):** Float setpoint - maintenance charge level
- **12.0V (Red):** Low battery warning - should rarely drop here

**Voltage Ranges (12V lead-acid/AGM):**
| Voltage | State of Charge | Assessment |
|---------|----------------|------------|
| 14.4-14.8V | 100% (charging) | Normal during absorption |
| 13.2-13.8V | 90-100% | Healthy resting voltage |
| 12.6-13.2V | 75-90% | Good operating range |
| 12.2-12.6V | 50-75% | Moderate discharge |
| 12.0-12.2V | 25-50% | Deep discharge - recharge soon |
| < 12.0V | < 25% | Critical - battery damage risk |

**What to look for:**
- **Green filled area shrinking** = Battery not reaching full charge
- **Red line frequently touched** = Undersized solar or excessive consumption
- **Min voltage dropping daily** = Battery degradation or insufficient charging

---

### Panel 4: Solar Panel Output (Middle Center)
**What it shows:** Peak PV power (orange) and voltage (blue) each day

**Understanding Panel Performance:**
- **Power spikes** = Cloud-edge effect (brief intense sunlight)
- **Consistent power** = Stable solar conditions
- **Low power** = Panel shading, dirt, or angle issues
- **High voltage, low power** = Panels getting light but not producing (dirty/failed cells)

**Voltage tells you:**
- **40-50V:** Panels in direct sunlight (typical for 100W panels in series)
- **30-40V:** Partial shade or low-angle sun
- **< 30V:** Heavy shading or panel issues

**Power optimization:**
- Your max is the panels' actual capability
- Compare to rated wattage (e.g., 100W panel should peak near 100W)
- Consistently below rating = cleaning needed or panel degradation

---

### Panel 5: MPPT Charging Phases (Middle Right)
**What it shows:** Time spent in each charging phase each day

**Charging Phases Explained:**

**🔴 Bulk (Red):**
- **What it is:** Fast charging phase when battery is low
- **What happens:** MPPT delivers maximum available power
- **Normal duration:** 1-6 hours depending on battery state and solar capacity
- **Long bulk times (>6 hrs)** = Undersized solar array or very discharged battery

**🟡 Absorption (Yellow):**
- **What it is:** Final charging to 100%, voltage held at 14.4V
- **What happens:** Current gradually decreases as battery fills
- **Normal duration:** 30 mins - 2 hours
- **Long absorption** = Battery sulfation or age-related issues
- **Short/no absorption** = Battery not reaching full charge

**🟢 Float (Green):**
- **What it is:** Maintenance mode, keeps battery topped off
- **What happens:** Voltage reduced to ~13.5V to prevent overcharge
- **Normal duration:** Rest of daylight hours after full charge
- **Long float times** = Good! Battery fully charged and maintained
- **No float** = Never reaching full charge (problem)

**Ideal Pattern:**
- Short bulk → Short absorption → Long float = Healthy, properly-sized system
- Long bulk → Short absorption → No float = Undersized solar
- Long bulk → Long absorption → Short float = Battery aging

---

### Panel 6: Cumulative Energy Production (Bottom Left)
**What it shows:** Total energy generated over time

**Analysis:**
- **Steep slope** = High daily production
- **Flat sections** = Low/no production days
- **Smooth curve** = Consistent performance
- **Step pattern** = Variable weather

**Use this to:**
- Project monthly/annual generation
- Calculate ROI and payback period
- Identify system reliability trends
- Compare summer vs winter performance

**Example calculation:**
- 30-day total: 1,900 Wh
- Daily average: 63 Wh/day
- Monthly projection: 1,900 Wh
- Annual projection: ~23,000 Wh (23 kWh)

---

### Panel 7: Charging Efficiency (Bottom Center)
**What it shows:** Average power delivered during charging (Wh per hour)

**Understanding Efficiency:**
- **High values (>50W)** = Good solar intensity during charging
- **Low values (<20W)** = Poor solar conditions or system issues
- **Consistent line** = Predictable system behavior
- **Erratic spikes** = Variable weather or panel shading

**Red dashed line** = Your system's average efficiency

**What affects efficiency:**
- ☀️ Sun angle and intensity
- 🌡️ Panel temperature (hotter = less efficient)
- 🔋 Battery state (fuller batteries charge slower)
- 🌥️ Cloud cover and shading
- 🧹 Panel cleanliness

**Troubleshooting:**
- Efficiency dropping over time = Panels need cleaning
- Very low efficiency = Check panel connections or MPPT settings

---

### Panel 8: Performance Insights (Bottom Right)
**What it shows:** Automated analysis and recommendations

**Insights Provided:**

**☀️ Production Analysis:**
- Days above average = System performing well
- Low production days = Weather or system issues
- Helps identify patterns (e.g., always low on Mondays = tree shade)

**🔋 Charging Pattern Analysis:**
- Average bulk time indicates solar sizing
- Long bulk (>5 hrs) = Need more panels
- Short bulk (<1 hr) = Oversized solar (good problem!)

**⚡ Battery Health Assessment:**
- Days below 12.2V = Battery stress
- Frequent deep discharge reduces battery lifespan
- Should be 0-2 days per month maximum

**📈 Recommendations:**
- **"Consider larger solar array"** = System undersized for battery
- **"Check battery capacity"** = Battery may be too small
- **"System performing well"** = Everything optimal
- **"Monitor during winter"** = Seasonal variations expected

---

## Interpreting Your Specific System

### Your 30-Day Data Shows:
Looking at your actual dashboard (if generated), here's what to focus on:

1. **Total Energy:** This is what your system actually produced
2. **Average Daily Yield:** Compare to your panel's rated capacity
   - 100W panel in good sun = 400-500 Wh/day
   - Your average shows actual performance

3. **Battery Voltage Patterns:** 
   - Are you reaching 14.4V regularly? (Full charge)
   - Are you dropping below 12.2V? (Deep discharge)

4. **Charging Phases:**
   - More float time = Better (battery getting fully charged)
   - More bulk time = System working hard (may need expansion)

---

## What Different Patterns Mean

### Healthy System Pattern:
✅ Consistent daily yields around average  
✅ Battery voltages stay between 12.4-14.4V  
✅ Long float times most days  
✅ Peak power close to panel rating  
✅ Few or no low production days  

### Warning Signs:
⚠️ Declining yield trend  
⚠️ Battery frequently below 12.2V  
⚠️ Never reaching float phase  
⚠️ Peak power much lower than rating  
⚠️ Many consecutive low-production days  

### Critical Issues:
❌ Battery dropping below 12.0V regularly  
❌ Zero production on sunny days  
❌ No absorption/float phases for weeks  
❌ Peak power < 30% of panel rating  
❌ Voltage spikes above 15V  

---

## Action Items Based on Dashboard

### If Your Dashboard Shows Low Production:
1. **Check panel cleanliness** - Dust, bird droppings, pollen
2. **Verify panel angle** - Should face equator, tilt = latitude
3. **Look for new shading** - Tree growth, new structures
4. **Inspect connections** - Corrosion, loose wires
5. **Check MPPT settings** - Battery type must match

### If Battery Health Looks Poor:
1. **Reduce loads** - Using more than generating
2. **Add solar capacity** - More panels or higher wattage
3. **Check battery condition** - May need replacement if old
4. **Verify wiring** - Voltage drop in cables
5. **Review settings** - Absorption voltage, float voltage

### If Charging Phases Are Off:
1. **Long bulk, no float** - Add solar panels
2. **No absorption** - Check MPPT absorption voltage setting
3. **Immediate float** - Battery not accepting charge (aging)
4. **No bulk** - Battery not discharging (no loads)

---

## Using This Data Over Time

### Weekly Monitoring:
- Check for sudden changes in production
- Verify battery voltages stay healthy
- Note any new patterns

### Monthly Analysis:
- Compare to previous months
- Track cumulative energy trends
- Identify seasonal patterns

### Seasonal Comparison:
- Summer vs winter production
- Sun angle effects
- Temperature impact on efficiency

### Annual Review:
- Calculate total production
- Assess system degradation (1-2% per year normal)
- Plan for expansions or upgrades
- Evaluate ROI and savings

---

## Quick Reference: Voltage Chart (12V System)

| Voltage | State | Action |
|---------|-------|--------|
| 14.7-15.0V | Equalization | Normal for flooded batteries only |
| 14.4-14.7V | Absorption | Final charging phase |
| 13.5-14.4V | Float | Maintenance, fully charged |
| 12.7-13.5V | Resting (Full) | 90-100% charged, healthy |
| 12.4-12.7V | Resting (Good) | 75-90% charged, normal |
| 12.2-12.4V | Half Charged | 50-75%, recharge soon |
| 12.0-12.2V | Low | 25-50%, recharge now |
| < 12.0V | Critical | Damage risk, immediate charge |

---

## Tips for Better Data

1. **Clean panels regularly** - Monthly in dusty areas
2. **Track weather** - Note cloudy periods in logs
3. **Monitor loads** - Know what's using power
4. **Check connections** - Corrosion reduces efficiency
5. **Update battery type in MPPT** - Wrong settings damage batteries
6. **Document changes** - Panel additions, battery replacements
7. **Compare to rated capacity** - Know your system's potential

---

## Need More Help?

### Understanding Your Results:
- Post your dashboard to r/solar or r/vandwellers
- Join Victron Community forums
- Compare with similar system owners

### Improving Performance:
- Victron VictronConnect app for detailed settings
- Solar calculators for expansion planning
- Battery monitoring for health assessment

### Professional Assessment:
- Solar installer for system audit
- Electrician for wiring issues
- Battery specialist for capacity testing

---

## Continuous Improvement

As you collect more data:
1. **Set up automated syncing** from Victron
2. **Track trends monthly** 
3. **Compare seasons**
4. **Optimize panel angles** for seasons
5. **Size battery bank** based on actual usage
6. **Plan expansions** with real data

Your dashboard evolves from a snapshot to a powerful tool for understanding and optimizing your solar system!
