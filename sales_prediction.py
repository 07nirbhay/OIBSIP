# -*- coding: utf-8 -*-
"""SALES PREDICTION

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/#fileId=https%3A//storage.googleapis.com/kaggle-colab-exported-notebooks/sales-prediction-fb10a439-2bec-4981-babe-02a970bc80bf.ipynb%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com/20240625/auto/storage/goog4_request%26X-Goog-Date%3D20240625T071006Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D1ab2910870816055cc1b42ccb18ad27a393510318f638ce7597a564ef07c86dd1ae7ce7549014878a3f8edfe041af66483d0ceff9805ea47e56881f0bfa1d83739cf56dfef469e4fa537f3cb68ebab6796964bc7f75550373f4396d5dc9c1f41bf2dc2e1adb0b6de9a5f916e8eda4c6566c73003caf4e0bf615560f26cf42deae3d230af902ed1b1239799d7f247057bbd5f632d66ee8a7d7069fb1d034076a3c91bfab0e11fec21e8b7e0d346f5b381602d8d44fbeb485bc3bbb37b3946e3f0a6392ed19bb1d399862335a5108ffed6fffc181ca9ef2d1d15539f952ff5d0e2fec03482191127ec2ebca3df68b2dabb6c62e23935004c255b00e19dcd64849b
"""

import os
import sys
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from urllib.parse import unquote, urlparse
from urllib.error import HTTPError
from zipfile import ZipFile
import tarfile
import shutil

CHUNK_SIZE = 40960
DATA_SOURCE_MAPPING = 'advertisingcsv:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F582088%2F1052144%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240625%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240625T071005Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D038bf51edbc461b606c0635c40d98ac48b6233f462ac230bd5a3c95cbfc4e89b84d95d976e43192e8e507f68352874769bf4f1bc6ef86183c8c2303a5ec283ed62f3eb930ec0d30d312e6f021d1bd78f2d8dd5ae16f33dc20e11c11d2b8600cfac36bbca456f1c84a1c18cd79a89c9226366a0f5c2f5217d875efc0d2ffb02dff52f31d312f0041dc0039e308c72c2bad962b2ad17c8d1fe018bb59a89debb76bd993e0dbd9079ed3c2a3e8743151de9ddb13331416b8f6958ca96c8a982d55b0bf964b71a33fb2050321ba5e6de0636a1383813f82dca2a594ebc72919a83184c593f4f28542dc0e88b5cc635e3f9794423d8e2bdb22cb8e7f73e9c09c37567'

KAGGLE_INPUT_PATH='/kaggle/input'
KAGGLE_WORKING_PATH='/kaggle/working'
KAGGLE_SYMLINK='kaggle'

!umount /kaggle/input/ 2> /dev/null
shutil.rmtree('/kaggle/input', ignore_errors=True)
os.makedirs(KAGGLE_INPUT_PATH, 0o777, exist_ok=True)
os.makedirs(KAGGLE_WORKING_PATH, 0o777, exist_ok=True)

try:
  os.symlink(KAGGLE_INPUT_PATH, os.path.join("..", 'input'), target_is_directory=True)
except FileExistsError:
  pass
try:
  os.symlink(KAGGLE_WORKING_PATH, os.path.join("..", 'working'), target_is_directory=True)
except FileExistsError:
  pass

for data_source_mapping in DATA_SOURCE_MAPPING.split(','):
    directory, download_url_encoded = data_source_mapping.split(':')
    download_url = unquote(download_url_encoded)
    filename = urlparse(download_url).path
    destination_path = os.path.join(KAGGLE_INPUT_PATH, directory)
    try:
        with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
            total_length = fileres.headers['content-length']
            print(f'Downloading {directory}, {total_length} bytes compressed')
            dl = 0
            data = fileres.read(CHUNK_SIZE)
            while len(data) > 0:
                dl += len(data)
                tfile.write(data)
                done = int(50 * dl / int(total_length))
                sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded")
                sys.stdout.flush()
                data = fileres.read(CHUNK_SIZE)
            if filename.endswith('.zip'):
              with ZipFile(tfile) as zfile:
                zfile.extractall(destination_path)
            else:
              with tarfile.open(tfile.name) as tarfile:
                tarfile.extractall(destination_path)
            print(f'\nDownloaded and uncompressed: {directory}')
    except HTTPError as e:
        print(f'Failed to load (likely expired) {download_url} to path {destination_path}')
        continue
    except OSError as e:
        print(f'Failed to load {download_url} to path {destination_path}')
        continue

print('Data source import complete.')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

data = pd.read_csv("/kaggle/input/advertisingcsv/Advertising.csv")

data.head(10)

data.info()

data.drop('Unnamed: 0', axis=1, inplace=True)

data.info()

rows, columns = data.shape
plt.figure(figsize=(6, 4))
plt.text(0.5, 0.5, f'Rows: {rows}\nColumns: {columns}', fontsize=12, ha='center', va='center')
plt.axis('off')
plt.title('DataFrame Dimensions')
plt.show()

data.head(20)

# @title Sales

from matplotlib import pyplot as plt
data['Sales'].plot(kind='hist', bins=20, title='Sales')
plt.gca().spines[['top', 'right',]].set_visible(False)

data.isnull().sum

data.describe()

from matplotlib import pyplot as plt
import seaborn as sns
_df_4.groupby('index').size().plot(kind='barh', color=sns.palettes.mpl_palette('Dark2'))
plt.gca().spines[['top', 'right',]].set_visible(False)

"""**Distribution of Sales**"""

plt.figure(figsize=(10, 6))
sns.histplot(data['Sales'], bins=30, kde=True)
plt.title('Distribution of Sales')
plt.xlabel('Sales')
plt.ylabel('Frequency')
plt.show()

"""**Pairplot to visualize relationships between numerical features**"""

sns.pairplot(data, vars=['TV', 'Radio', 'Newspaper', 'Sales'])
plt.title(' Numerical Features Pairplot ')
plt.show()

"""**Correlation heatmap**"""

plt.figure(figsize=(8, 6))
correlation_matrix = data[['TV', 'Radio', 'Newspaper', 'Sales']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap')
plt.show()

"""**Create subplots for each histogram**"""

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Plot histograms for 'TV,' 'Radio,' and 'Newspaper' columns
data["TV"].plot.hist(ax=axes[0], bins=10, color='skyblue', edgecolor='black')
axes[0].set_title('TV Advertising Budget')
axes[0].set_xlabel('Spending')
axes[0].set_ylabel('Frequency')

data["Radio"].plot.hist(ax=axes[1], bins=10, color='lightcoral', edgecolor='black')
axes[1].set_title('Radio Advertising Budget')
axes[1].set_xlabel('Spending')
axes[1].set_ylabel('Frequency')

data["Newspaper"].plot.hist(ax=axes[2], bins=10, color='lightgreen', edgecolor='black')
axes[2].set_title('Newspaper Advertising Budget')
axes[2].set_xlabel('Spending')
axes[2].set_ylabel('Frequency')

plt.tight_layout()
plt.show()

"""**training and testing**"""

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(data[["TV"]], data[["Sales"]], test_size=0.3, random_state=42)

"""**Create a linear regression model**"""

from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(x_train,y_train)

"""**predictions on the test data**"""

predictions = model.predict(x_test)

"""**Plot the regression line**"""

plt.figure(figsize=(8, 6))
plt.scatter(x_test, y_test, color='blue', label='Actual Sales')
plt.plot(x_test, predictions, color='red', linewidth=2, label='Predicted Sales')
plt.title('Linear Regression - TV Advertising vs. Sales')
plt.xlabel('TV Advertising Budget')
plt.ylabel('Sales')
plt.legend()
plt.show()