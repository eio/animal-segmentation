import torch
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Setup output paths
SAVED_MODEL_PATH = "results/model+optimizer.pth"
LOSS_PLOT_PATH = "figures/loss.png"
PREDICTIONS_DIR = "predictions/"


def save_model(epoch, net, optimizer):
    """
    Save the current state of the Model
    so we can load the latest state later on
    https://pytorch.org/tutorials/beginner/saving_loading_models.html
    """
    torch.save(
        {
            "epoch": epoch,
            "model_state_dict": net.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
        },
        SAVED_MODEL_PATH,
    )


def load_model():
    """
    Load and return the saved, pre-trained Model and Optimizer
    """
    print("Loading the saved model: `{}`".format(SAVED_MODEL_PATH))
    saved_state = torch.load(SAVED_MODEL_PATH)
    net = Net().to(DEVICE)
    optimizer = Optimizer(net)
    net.load_state_dict(saved_state["model_state_dict"])
    optimizer.load_state_dict(saved_state["optimizer_state_dict"])
    print("Model loaded.")
    return net, optimizer


def write_output_csv(epoch, predictions, fieldnames):
    """
    Write model predictions to output CSV
    """
    csv_name = "predictions_epoch{}.csv".format(epoch)
    output_csv = PREDICTIONS_DIR + csv_name
    print("Write the predicted output to: {}...".format(output_csv))
    with open(output_csv, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        for i in range(0, len(predictions)):
            writer.writerow(predictions[i])


def plot_loss(completed_epochs, avg_train_losses, avg_test_losses):
    """
    Generate a plot showing the loss-per-epoch
    for both the training and test datasets
    """
    fig = plt.figure()
    ax = fig.gca()
    plt.scatter(completed_epochs, avg_train_losses, color="blue")
    plt.scatter(completed_epochs, avg_test_losses, color="red")
    plt.legend(["Train Loss", "Test Loss"], loc="upper right")
    plt.xlabel("Number of Epochs")
    plt.ylabel("Cross Entropy (CE) Loss")
    # Force integer X-axis tick marks,
    # since fractional epochs aren't a thing
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.savefig(LOSS_PLOT_PATH)
    print("Performance evaluation saved to: `{}`".format(LOSS_PLOT_PATH))
