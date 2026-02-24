def cpu_notification():
    if cpu_logging == "":
        cpu_logging = cpu_status
    elif cpu_logging != cpu_status:
        with open(text.file, 'rb') as fp:
            msg = MIMEText(fp.read())
        msg['Betreff'] = 'Monitoring Warning CPU '+ cpu_logging
        msg['Von'] = sender
        msg['An'] = adresser

        s = smtplib.SMTP('localhost')
        s.sendmail(sender, [adresser], msg.as_string())
        s.quit()

        cpu_logging = cpu_status
    else:
        with open(text.file, 'rb') as fp:
            msg = MIMEText(fp.read())
        msg['Betreff'] = 'Somthing want wrong'
        msg['Von'] = sender
        msg['An'] = adresser
