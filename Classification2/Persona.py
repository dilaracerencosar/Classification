# The Calculation of Potential Customer Revenue with Rule-Based Classification

#####
# A game company creates new level-based customer definitions (personas) using some of its customers' characteristics.
# to create segments according to these new customer definitions and to identify new customers who may come to the company according to these segments.
# They want to estimate how much he can earn on average.

# For example: It is desired to determine how much money a 25-year-old male user from Turkiye, who is an IOS user, can earn on average.


#####
# Dataset Story
#####
# Persona.csv data set shows the prices of the products sold by an international game company and some of the users who purchased these products.
# It contains demographic information. The dataset consists of records created in each sales transaction.
# This means table not deduplicated. In other words, a user with certain demographic characteristics may have made more than one purchase.

# Price: Customer's spending amount
# Source: The type of device the customer is connected to
# Sex: Customer's gender
# Country: Customer's country
# Age: Customer's age

################# Before Application #####################

#    PRICE   SOURCE   SEX COUNTRY  AGE
# 0     39  android  male     bra   17
# 1     39  android  male     bra   17
# 2     49  android  male     bra   17
# 3     29  android  male     tur   17
# 4     49  android  male     tur   17

################# After Application #####################

#       customers_level_based        PRICE SEGMENT
# 0   BRA_ANDROID_FEMALE_0_18  1139.800000       A
# 1  BRA_ANDROID_FEMALE_19_23  1070.600000       A
# 2  BRA_ANDROID_FEMALE_24_30   508.142857       A
# 3  BRA_ANDROID_FEMALE_31_40   233.166667       C
# 4  BRA_ANDROID_FEMALE_41_66   236.666667       C


# Read the persona.csv file and show general information about the data set.
import pandas as pd
pd.set_option("display.max_rows", None)
df = pd.read_csv(r'C:\Users\Dilara Ceren Coşar\OneDrive\Masaüstü\datasets\persona.csv')
df.head()
df.shape
df.info()

# How many unique SOURCE are there? What are their frequencies?
df["SOURCE"].nunique()
df["SOURCE"].value_counts()

# How many unique PRICEs are there?
df["PRICE"].nunique()

# How many sales were made from which PRICE?
df["PRICE"].value_counts()

# How many sales were made from which country?
df["COUNTRY"].value_counts()
df.groupby("COUNTRY")["PRICE"].count()

df.pivot_table(values="PRICE",index="COUNTRY",aggfunc="count")


# How much was earned from sales in total by country?
df.groupby("COUNTRY")["PRICE"].sum()
df.groupby("COUNTRY").agg({"PRICE": "sum"})

df.pivot_table(values="PRICE",index="COUNTRY",aggfunc="sum")

# What are the sales numbers according to SOURCE types?
df["SOURCE"].value_counts()

# What are the PRICE averages by country?
df.groupby(by=['COUNTRY']).agg({"PRICE": "mean"})

# What are the PRICE averages according to SOURCEs?
df.groupby(by=['SOURCE']).agg({"PRICE": "mean"})

# What are the PRICE averages in the COUNTRY-SOURCE breakdown?
df.groupby(by=["COUNTRY", 'SOURCE']).agg({"PRICE": "mean"})



# What are the average earnings in the COUNTRY, SOURCE, SEX, AGE breakdown?
df.groupby(["COUNTRY", 'SOURCE', "SEX", "AGE"]).agg({"PRICE": "mean"}).head()



# Sort the output by PRICE.
# To better see the output in the previous question, apply the sort_values method to PRICE in decreasing order.
# Save the output as agg_df.
agg_df = df.groupby(by=["COUNTRY", 'SOURCE', "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values("PRICE", ascending=False)
agg_df.head()



# Convert the names in the index into variable names.
# All variables except PRICE in the output of the third question are index names.
# Convert these names to variable names.
# Hint: reset_index()
# agg_df.reset_index(inplace=True)
agg_df = agg_df.reset_index()
agg_df.head()



# Convert the AGE variable to a categorical variable and add it to agg_df.
# Convert the numeric variable Age to a categorical variable.
# Create the intervals in a way that you think will be convincing.
# Example: '0_18', '19_23', '24_30', '31_40', '41_70'

# Let's specify where the AGE variable will be divided:
bins = [0, 18, 23, 30, 40, agg_df["AGE"].max()]

# Let's express what the naming will be in response to the divided points:
mylabels = ['0_18', '19_23', '24_30', '31_40', '41_' + str(agg_df["AGE"].max())]

# Let's divide age:
agg_df["age_cat"] = pd.cut(agg_df["AGE"], bins, labels=mylabels)
agg_df.head()



# Define new level based customers and add them to the data set as a variable.
# Define a variable called customers_level_based and add this variable to the data set.
# Attention! After creating customers_level_based values with list comp, these values need to be deduplicated.
# For example, there may be more than one of: USA_ANDROID_MALE_0_18
# It is necessary to take these to groupby and get the price average.


# method 2
agg_df['customers_level_based'] = agg_df[['COUNTRY', 'SOURCE', 'SEX', 'age_cat']].agg(lambda x: '_'.join(x).upper(), axis=1)


# method 3
agg_df["customers_level_based"] = ['_'.join(i).upper() for i in agg_df.drop(["AGE", "PRICE"], axis=1).values]


# method 1
# variable names:
agg_df.columns

# How to access observation values?
for row in agg_df.values:
    print(row)

# We want to put the VALUES of the variables COUNTRY, SOURCE, SEX and age_cat next to each other and combine them with an underscore.
# We can do this with list comprehension.
# Let's perform the process to select the observation values in the loop above that we need:
[row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]

# Let's add it to the data set:
agg_df["customers_level_based"] = [row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]
agg_df.head()

# Let's remove unnecessary variables:
agg_df = agg_df[["customers_level_based", "PRICE"]]
agg_df.head()

for i in agg_df["customers_level_based"].values:
    print(i.split("_"))


# We are one step closer to our goal.
# There's a little problem here. There will be many of the same segments.
# can be multiple, for example segment USA_ANDROID_MALE_0_18.
# let's check:
agg_df["customers_level_based"].value_counts()

# For this reason, after groupby by segments, we should take the price averages and deduplicate the segments.
agg_df = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"})

# It is located in the customers_level_based index. Let's turn this into a variable.
agg_df = agg_df.reset_index()
agg_df.head()

# Let's check. We expect each persona to have 1:
agg_df["customers_level_based"].value_counts()
agg_df.head()


# Segment new customers (USA_ANDROID_MALE_0_18).
# Segment by PRICE, add the segments to agg_df with the name "SEGMENT", describe the segments,
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
agg_df.head(30)
agg_df.groupby("SEGMENT").agg({"PRICE": "mean"})




# Classify new customers and estimate how much income they can bring.
# To which segment does a 33-year-old Turkish woman using ANDROID belong and how much income is she expected to earn on average?
new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]

# In which segment and how much income on average is a 35-year-old French woman using IOS expected to earn?
new_user = "FRA_IOS_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]
