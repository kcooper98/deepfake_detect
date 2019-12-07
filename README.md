CNN_Test3 has latest iteration of basic model (that was used to make the two models above)


RealTestingImages has set of real images that we can use to test our models. Same for FakeTestingImages


Datasets not added to github repo due to space constraints.


CNNModel has saved model that was trained using CNN_Test3 using 2000 images (1000 of each class) on NVIDIA generated images
* 50 epochs
* 25 steps per epoch
* 5 validation steps


CNNModel4000Set trained using 4000 images (2000 of each class) on NVIDIA images (located in HardData2) and 500 each validation images
* 50 epochs
* 25 steps per epoch
* 5 validation steps


web_app.py contains python code for creating the Flask server.\
static folder contains web templates, css code for styling, and server uploads.