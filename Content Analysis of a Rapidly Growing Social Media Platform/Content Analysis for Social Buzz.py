#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# ### Loading the content dataset and making a copy of the original

# In[2]:


content = pd.read_csv(r"D:\Data Science\PROJECTS\Accenture Project\Task 2\Content.csv")
content


# In[3]:


content_copy = content.copy()


# In[4]:


content_copy


# In[5]:


content_copy.info()


# #### Dropping the 'Unnamed: 0' column

# In[6]:


content_copy.drop(['Unnamed: 0'], axis=1, inplace=True)
content_copy


# #### Dropping the URL column

# In[7]:


content_copy.drop(['URL'], axis=1, inplace=True)
content_copy


# In[8]:


content_copy['Category'].value_counts()


# #### Cleaning up the Categories.

# In[9]:


content_copy['Category'] = content_copy['Category'].str.lower().str.replace(r'["]', '')


# In[10]:


content_copy['Category'].value_counts()


# In[11]:


content_copy


# #### Renaming the Type column for uniformity among datasets

# In[12]:


content_copy.rename(columns={'Type': 'Content Type'}, inplace=True)


# In[13]:


content_copy


# #### Dropping the User ID column

# In[14]:


content_copy.drop(['User ID'], axis=1, inplace=True)


# In[15]:


content_copy


# ### Loading the reactions dataset and making a copy of the original

# In[16]:


reactions = pd.read_csv(r"D:\Data Science\PROJECTS\Accenture Project\Task 2\Reactions.csv")
reactions_copy = reactions.copy()
reactions_copy


# In[17]:


reactions_copy.info()


# #### Dropping the 'Unnamed: 0' column

# In[18]:


reactions_copy.drop(['Unnamed: 0'], axis=1, inplace=True)
reactions_copy


# #### Converting the Datetime column to a datetime dtype for better manipulation

# In[19]:


reactions_copy['Datetime'] = pd.to_datetime(reactions_copy['Datetime'])
reactions_copy


# In[20]:


reactions_copy.info()


# #### Dropping the User ID Column

# In[21]:


reactions_copy.drop(['User ID'], axis=1, inplace=True)
reactions_copy


# #### Deleting the NaN values from the Type Column and renaming it as well for uniformity

# In[22]:


reactions_copy.isnull().sum()


# In[23]:


reactions_copy.dropna(subset=['Type'], axis=0, inplace=True)


# In[24]:


reactions_copy


# In[25]:


reactions_copy.info()


# In[26]:


reactions_copy.rename(columns={'Type': 'Reaction Type'}, inplace=True)
reactions_copy


# ### Loading the reaction type dataset and making a copy of the original 

# In[27]:


reactiontype = pd.read_csv(r"D:\Data Science\PROJECTS\Accenture Project\Task 2\ReactionTypes.csv")
reactiontype_copy = reactiontype.copy()
reactiontype_copy


# #### Dropping the 'Unnamed: 0' column

# In[28]:


reactiontype_copy.drop(['Unnamed: 0'], axis=1, inplace=True)
reactiontype_copy


# #### Renaming the Type column for uniformity

# In[29]:


reactiontype_copy.rename(columns={'Type': 'Reaction Type'}, inplace=True)


# In[30]:


reactiontype_copy


# In[31]:


reactions_copy.info()


# ### Creating a Final Data Set

# In[32]:


content_copy


# In[33]:


reactions_copy


# In[34]:


reactiontype_copy


# In[35]:


final_data_set = pd.merge(reactions_copy, content_copy, left_on='Content ID',
                          right_on='Content ID', how='inner')
final_data_set


# In[36]:


final_data_set = pd.merge(final_data_set, reactiontype_copy, left_on= 'Reaction Type',
                          right_on='Reaction Type', how='left')
final_data_set


# #### Figuring out the Top 5 performing categories

# In[37]:


popular_categories = final_data_set.groupby('Category')['Score'].sum().sort_values(ascending=False)


# In[38]:


popular_categories


# In[39]:


top5 = popular_categories.head()
top5


# #### Exporting the final data and the popular categories into a single file

# In[40]:


with pd.ExcelWriter("D:\Data Science\PROJECTS\Accenture Project\Task 2\Final Data.xlsx") as writer:
    final_data_set.to_excel(writer, sheet_name='Cleaned Data')
    top5.to_excel(writer, sheet_name='Top 5 Popular Categories')


# ### Visualisation Of The Data

# In[40]:


final_data_set


# #### Q. What are the Top 5 Categories based on Collective Score?

# In[41]:


plt.figure(figsize=(8,5))

fig1 = top5.plot(kind='bar')
plt.xlabel('Category')
plt.ylabel('Total Score')
plt.xticks(rotation=0)
plt.ylim(0,80000)

for index, value in enumerate(top5):
    plt.annotate(value, (index,value), ha='center', va='bottom')

plt.title('Top 5 Categories based on Collective Score')
plt.savefig("Top 5 Categories based on Collective Score.png")


# ##### We can clearly see the top 5 categories based on the collective scores are:
# 1. Animals
# 2. Science
# 3. Healthy Eating
# 4. Technology
# 5. Food

# #### Q. How many unique categories are there?

# In[42]:


plt.figure(figsize=(10,6))

fig2 = sns.countplot(y='Category', data=final_data_set)
plt.title("Unique Categories")

plt.savefig('Unique Categories.png')


# In[43]:


len(final_data_set['Category'].value_counts())


# ##### The number of unique categories are 16 in total  ranging from studying till culture

# #### Q. How many reactions are there to the most popular category?

# In[45]:


animal_df = final_data_set[final_data_set['Category'] == 'animals']
animal_df


# In[46]:


plt.figure(figsize=(10,5))

fig3 = sns.countplot(x='Reaction Type', data=animal_df)
plt.xticks(rotation=45, ha='right')
plt.xlabel('Reaction Type')
plt.ylabel('Count')
plt.ylim(0,150)

for patch in fig3.patches:
    x_coor = patch.get_x()
    value = patch.get_height()
    fig3.annotate(value, (x_coor, value), va='bottom', ha='left')
    
plt.title(f'Reaction Type Distribution in Most Popular Category: Animal')
plt.savefig("Reaction Type Distribution Of The Most Popular Category.png")


# ##### Here we can see the different reaction type to the most popular category i.e: Animal

# #### What was the month with the most posts?

# In[48]:


final_data_set['months'] = final_data_set['Datetime'].dt.month
final_data_set


# In[50]:


plt.figure(figsize=(10,5))

fig4 = sns.countplot(x='months', data=final_data_set)
plt.ylim(0,2500)

for patch in fig4.patches:
    x_coor = patch.get_x()
    value = patch.get_height()
    plt.annotate(value, (x_coor, value), va='bottom', ha='left')

plt.title("Most Frequent Month")
plt.savefig("Most no. of posts in a month.png")


# ##### Here we can see the month with the most number of posts is: May

# In[ ]:




