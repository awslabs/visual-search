import os
import greengrasssdk
import awscam
import mo
import cv2


client = greengrasssdk.client('iot-data')
iot_topic = '$aws/things/{}/infer'.format(os.environ['AWS_IOT_THING_NAME'])


def greengrass_infinite_infer_run():

    input_height = 224
    input_width = 224
    model_name = 'featurizer-v1'
    error, model_path = mo.optimize(model_name, input_width, input_height)

    if error != 0:
        client.publish(topic=iot_topic, payload="Model optimization FAILED")
    else:
        client.publish(topic=iot_topic, payload="Model optimization SUCCEEDED")

    model = awscam.Model(model_path, {"GPU" : 1})
    client.publish(topic=iot_topic, payload="Model loaded SUCCESSFULLY")

    while True:
        ret, frame = awscam.getLastFrame()
        if not ret:
            client.publish(topic=iot_topic, payload="FAILED to get frame")
        else:
            client.publish(topic=iot_topic, payload="frame retrieved")

        frame_resize = cv2.resize(frame, (input_width, input_height))
        infer_output = model.doInference(frame_resize)
        features_numpy = None
        for _, val in infer_output.iteritems():
            features_numpy = val

        features_string = ','.join(str(e) for e in features_numpy)
        msg = '{ "features": "' + features_string + '" }'
        client.publish(topic=iot_topic, payload=msg)


greengrass_infinite_infer_run()


def function_handler(event, context):
    return
