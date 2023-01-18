import modal
from Training_data_transformation import get_training_data
import os
LOCAL=False

if LOCAL == False:
   stub = modal.Stub("model-training")
   image = modal.Image.debian_slim().apt_install(["libgomp1"]).pip_install(["joblib","hopsworks", "seaborn", "joblib", "scikit-learn","xgboost"])

   @stub.function(image=image, schedule=modal.Period(days=1), secret=modal.Secret.from_name("lab1"))
   def f():
       g()

def g():
    import hopsworks
    import pandas as pd
    from sklearn.metrics import mean_squared_error as MSE
    from sklearn.model_selection import train_test_split
    from xgboost import XGBRegressor
    import joblib
    from hsml.schema import Schema
    from hsml.model_schema import ModelSchema
    

    train_df=get_training_data()
    y=train_df["aqi"]
    x=train_df.drop(["aqi","datetime"],axis=1)
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.05, random_state=42)
    model=XGBRegressor()
    model.fit(x_train,y_train)
    performance=MSE(y_test,model.predict(x_test))

    model_dir="aqi_model"
    if os.path.isdir(model_dir)==False:
        os.mkdir(model_dir)
    joblib.dump(model,model_dir+"/aqi_model.plk")
    
    input_schema = Schema(x_train)
    output_schema = Schema(y_train)
    
    model_schema = ModelSchema(input_schema, output_schema)

    project=hopsworks.login(project="test42")
    mr = project.get_model_registry()

    aqi_model = mr.python.create_model(
        name="aqi_model_modal", 
        metrics={"mean_squared_error" : performance},
        model_schema=model_schema,
        description="Air Quality Forecast"
    )
    aqi_model.save(model_dir)
    print("MODEL DEPLOYED")
    
if __name__ == "__main__":
    if LOCAL == True :
        g()
    else:
        stub.deploy("model-training")
        with stub.run():
            f()
