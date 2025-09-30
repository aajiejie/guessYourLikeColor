# Project Name
Guess Your Favorite Colors

# Project Description
Generate color combinations based on three dimensions: color system, saturation, and color matching. Then adjust preferences through yes/no buttons.

# Content
![img_1.png](img_1.png)
![img.png](img.png)

Simply click yes or no. After several clicks, it becomes increasingly accurate at guessing your favorite colors.

# Configuration Files

## 1. Preference Configuration

**File:** `src/users/myUser.json`

**Persistent preference tracking:**
- Initial value: 100
- Each yes/no click modifies corresponding scores

**Dimensions tracked:**
1. **Color System** (Red, Orange, Yellow, Green, Aqua, Blue, Purple)
2. **Saturation** (High, Medium, Low) 
3. **Color Matching** (Monochromatic, Analogous, Complementary, Triadic)

## 2. Color Configuration

**File:** `src/colorConfig.py`

**Combines color system and saturation to form a color table:**

🔴 **Red Color System**
Saturation | RGB Values | Color Preview
-----------|------------|--------------
High Saturation | (255, 179, 191) | <div style="width:120px;height:40px;background-color:rgb(255,179,191);border:1px solid #ddd"></div>
Medium Saturation | (255, 179, 179) | <div style="width:120px;height:40px;background-color:rgb(255,179,179);border:1px solid #ddd"></div>
Low Saturation | (255, 242, 242) | <div style="width:120px;height:40px;background-color:rgb(255,242,242);border:1px solid #ddd"></div>

🟠 **Orange Color System**
Saturation | RGB Values | Color Preview
-----------|------------|--------------
High Saturation | (255, 209, 179) | <div style="width:120px;height:40px;background-color:rgb(255,209,179);border:1px solid #ddd"></div>
Medium Saturation | (255, 223, 204) | <div style="width:120px;height:40px;background-color:rgb(255,223,204);border:1px solid #ddd"></div>
Low Saturation | (255, 242, 230) | <div style="width:120px;height:40px;background-color:rgb(255,242,230);border:1px solid #ddd"></div>

🟡 **Yellow Color System**
Saturation | RGB Values | Color Preview
-----------|------------|--------------
High Saturation | (255, 247, 204) | <div style="width:120px;height:40px;background-color:rgb(255,247,204);border:1px solid #ddd"></div>
Medium Saturation | (255, 249, 204) | <div style="width:120px;height:40px;background-color:rgb(255,249,204);border:1px solid #ddd"></div>
Low Saturation | (255, 252, 242) | <div style="width:120px;height:40px;background-color:rgb(255,252,242);border:1px solid #ddd"></div>

🟢 **Green Color System**
Saturation | RGB Values | Color Preview
-----------|------------|--------------
High Saturation | (219, 255, 237) | <div style="width:120px;height:40px;background-color:rgb(219,255,237);border:1px solid #ddd"></div>
Medium Saturation | (234, 255, 242) | <div style="width:120px;height:40px;background-color:rgb(234,255,242);border:1px solid #ddd"></div>
Low Saturation | (231, 255, 239) | <div style="width:120px;height:40px;background-color:rgb(231,255,239);border:1px solid #ddd"></div>

🔵 **Aqua Color System**
Saturation | RGB Values | Color Preview
-----------|------------|--------------
High Saturation | (204, 255, 247) | <div style="width:120px;height:40px;background-color:rgb(204,255,247);border:1px solid #ddd"></div>
Medium Saturation | (217, 255, 255) | <div style="width:120px;height:40px;background-color:rgb(217,255,255);border:1px solid #ddd"></div>
Low Saturation | (217, 255, 255) | <div style="width:120px;height:40px;background-color:rgb(217,255,255);border:1px solid #ddd"></div>

🔷 **Blue Color System**
Saturation | RGB Values | Color Preview
-----------|------------|--------------
High Saturation | (204, 229, 255) | <div style="width:120px;height:40px;background-color:rgb(204,229,255);border:1px solid #ddd"></div>
Medium Saturation | (220, 229, 255) | <div style="width:120px;height:40px;background-color:rgb(220,229,255);border:1px solid #ddd"></div>
Low Saturation | (217, 217, 255) | <div style="width:120px;height:40px;background-color:rgb(217,217,255);border:1px solid #ddd"></div>

🟣 **Purple Color System**
Saturation | RGB Values | Color Preview
-----------|------------|--------------
High Saturation | (160, 32, 240) | <div style="width:120px;height:40px;background-color:rgb(160,32,240);border:1px solid #ddd"></div>
Medium Saturation | (181, 126, 220) | <div style="width:120px;height:40px;background-color:rgb(181,126,220);border:1px solid #ddd"></div>
Low Saturation | (255, 229, 255) | <div style="width:120px;height:40px;background-color:rgb(255,229,255);border:1px solid #ddd"></div>

# Scoring System

- **Click YES:** Increase score
  - **Upper limit:** Average of other values in the same dimension × 1.5
    
- **Click NO:** Decrease score
  - **Lower limit:** 25
    
- **Set upper and lower limits:** To give other low-scoring options probability space to appear, adding more freshness
    
- **Decrease points more than increase points:** To quickly eliminate disliked factors