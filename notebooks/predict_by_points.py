import numpy as np
import torch
import matplotlib.pyplot as plt
import cv2
import sys

# sys.path.append("..")
from segment_anything import sam_model_registry, SamPredictor


def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)


def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels == 1]
    neg_points = coords[labels == 0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white',
               linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white',
               linewidth=1.25)


def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0, 0, 0, 0), lw=2))


image = cv2.imread('images/truck.jpg')
# print(image)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

sam_checkpoint = "../sam_vit_b_01ec64.pth"
# sam_checkpoint = "sam_vit_b_01ec64.pth"
model_type = "vit_b"

device = "cuda"

sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)

predictor = SamPredictor(sam)
# 得到image_embedding
predictor.set_image(image)

input_point = np.array([[500, 375], [500, 370], [1125, 625]])
input_label = np.array([1, 1, 0])
# input_box = np.array([425, 600, 700, 875])

# plt.figure(figsize=(10, 10))
# plt.imshow(image)
# show_points(input_point, input_label, plt.gca())
# plt.axis('on')
# plt.show()

masks, scores, logits = predictor.predict(
    point_coords=input_point,
    point_labels=input_label,
    # box=input_box[None, :],
    multimask_output=True,
)

# for i, (mask, score) in enumerate(zip(masks, scores)):
#     plt.figure(figsize=(10, 10))
#     plt.imshow(image)
#     show_mask(mask, plt.gca())
#     show_points(input_point, input_label, plt.gca())
#     plt.title(f"Mask {i + 1}, Score: {score:.3f}", fontsize=18)
#     plt.axis('off')
#     plt.show()
