if cpu_usage["total"] >= 90:
        cpu_status = "Critical"
    elif cpu_usage["total"] >= 80:
        cpu_status = "Warning"
    elif cpu_usage["total"] <= 80:
        cpu_status = "Okay"
    else:
        with open(text.file, 'rb') as fp:
            msg = MIMEText(fp.read())
        msg['Betreff'] = 'Unable to read CPU status' 
        msg['Von'] = sender
        msg['An'] = adresser

        s = smtplib.SMTP('localhost')
        s.sendmail(sender, [adresser], msg.as_string())
        s.quit()
        break
