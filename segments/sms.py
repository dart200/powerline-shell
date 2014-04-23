def add_sms_segment():
    if os.environ.get('SMSCHROOT'):
        host_prompt = ' %s ' % os.environ.get("SMSCHROOT").split("/")[-1]
        powerline.append(host_prompt, Color.SMS_FG, Color.SMS_BG)

add_sms_segment()
