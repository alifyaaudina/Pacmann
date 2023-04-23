#!/usr/bin/env python
# coding: utf-8

# In[1]:


import module


# In[2]:


trx01 = module.transaction()


# In[3]:


trx01.add_item('Ayam Goreng',2, 20000)
trx01.add_item('Pasta Gigi', 3, 15000)
trx01.add_item('Gayung Mandi', 20, 10000)


# In[4]:


trx01.update_item_name('Ayam Goreng', "Apel Fuji")


# In[5]:


trx01.update_item_qty('Gayung Mandi', 100)


# In[6]:


trx01.update_item_qty('Gayung', 73)


# In[7]:


trx01.update_item_price("Apel Fuji",30000)


# In[8]:


trx01.delete_item("Pasta Gigi")


# In[23]:


trx01.reset_transaction()


# In[24]:


trx01.add_item('Kecap Manis',2, 14000)
trx01.add_item('Set Piyama Anak', 3, 70000)
trx01.add_item('Topi Baseball', 7, 60000)
trx01.add_item('Panci Air', "Tujuh", 20000)


# In[25]:


trx01.check_order()


# In[26]:


trx01.update_item_qty('Panci Air', 7)


# In[27]:


trx01.check_order()


# In[28]:


trx01.check_out()

