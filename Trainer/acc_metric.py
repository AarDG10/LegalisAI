import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, recall_score, confusion_matrix

# Ground truth sections (relevant sections for this case)
true_sections = [
    "Section 3 - Maharashtra Ownership Flats (MOFA) Act, 1963",
    "Section 4 - Maharashtra Ownership Flats (MOFA) Act, 1963",
    "Section 13(1) - Real Estate (Regulation and Development) Act, 2016 (RERA)",
    "Section 10 - Maharashtra Ownership Flats (MOFA) Act, 1963"
]

# Predicted sections (sections retrieved by your model)
predicted_sections = [
    "Section 3 - Maharashtra Ownership Flats (MOFA) Act, 1963",
    "Section 4 - Maharashtra Ownership Flats (MOFA) Act, 1963",
    "Section 14 - Real Estate (Regulation and Development) Act, 2016 (RERA)",
    "Section 8 - Maharashtra Ownership Flats (MOFA) Act, 1963",
    "Section 17 - Maharashtra Ownership Flats (MOFA) Act, 1963"
]

# Convert sections to binary values
y_true_binary = [1 if section in true_sections else 0 for section in true_sections + predicted_sections]
y_pred_binary = [1 if section in predicted_sections else 0 for section in true_sections + predicted_sections]

# Calculate precision and recall
precision = precision_score(y_true_binary, y_pred_binary)
recall = recall_score(y_true_binary, y_pred_binary)

# Print precision and recall
print(f"Jaccard Precision: {precision:.4f}")
print(f"Jaccard Recall: {recall:.4f}")

# Calculate confusion matrix
conf_matrix = confusion_matrix(y_true_binary, y_pred_binary)

# Visualize the confusion matrix using Matplotlib
plt.figure(figsize=(8, 6))
plt.imshow(conf_matrix, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Jaccard Confusion Matrix')
plt.colorbar()
tick_marks = np.arange(2)
plt.xticks(tick_marks, ['Predicted No', 'Predicted Yes'])
plt.yticks(tick_marks, ['True No', 'True Yes'])

# Label each cell with the numeric value
thresh = conf_matrix.max() / 2.
for i, j in np.ndindex(conf_matrix.shape):
    plt.text(j, i, format(conf_matrix[i, j], 'd'),
             horizontalalignment="center",
             color="white" if conf_matrix[i, j] > thresh else "black")

plt.ylabel('True')
plt.xlabel('Predicted')
plt.tight_layout()
plt.show()
