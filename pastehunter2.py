#!/usr/bin/env python3
import sys
import time
import logging
import signal
import threading
import json

import smtplib
from email.mime.text import MIMEText
from clockwork import clockwork

import phparsers
import digestPaste
from config import config, clockworkapi


def exit_gracefully(*_):
    logging.info("SIGINT caught, Waiting for last paste to be parsed")
    ev.set()


def sendtext(msg, phone):
    for m in [msg[i:i + 10] for i in range(0, len(msg), 10)]:
        m = "Urgent filter triggered for:\n" + "\n".join(m)
        message = clockwork.SMS(from_name="Pastehunter", to=phone,
                                message=m)
        response = clockworkapi.send(message)
        if response.success:
            logging.warning("Urgent text sent!")
        else:
            logging.error("Something wrong with texting -> (%s)",
                          response.error_message)


def sendReports(reports, phone, email):

    alert_email_account = config["smtp"]["login"]
    alert_email_password = config["smtp"]["password"]

    email_body = "The following are keyword hits that were just found:\n\n"

    msg = []
    for report in reports:
        if not report.urgent:
            email_body += str(report)
            email_body += "\n---\n"
        else:
            msg.append(report.getURL())

    if msg: # 10
        sendtext(msg, phone)

    msg = MIMEText(email_body)
    msg['Subject'] = "Alert Email"
    msg['From'] = alert_email_account
    msg['To'] = email

    server = smtplib.SMTP(config["smtp"]["smtp"], config["smtp"]["port"])
    # server.set_debuglevel(True)

    server.ehlo()
    server.starttls()
    server.login(alert_email_account, alert_email_password)
    server.sendmail(alert_email_account,
                    alert_email_account, msg.as_string())
    server.quit()

    logging.info("Report sent!")


def updateJson(filterFile, ftype, regex, urgent, desc):

    with open(filterFile, 'r') as fin:
        try:
            jsonFilters = json.loads(fin.read())
        except json.decoder.JSONDecodeError as e:
            logging.error("Malformed json file %s", e)

    if ftype in jsonFilters:
        jsonFilters[ftype].append({"regex": regex,
                                   "urgent": urgent,
                                   "desc": desc})
    else:
        jsonFilters[ftype] = [{"regex": regex,
                               "urgent": urgent,
                               "desc": desc}]

    with open(filterFile, 'w') as fout:
        json.dump(jsonFilters, fout,
                  sort_keys=True,
                  indent=4,
                  separators=(',', ': '))


def loadCsv(csv, filterFile):

    with open(csv, 'r') as fin:
        headers = fin.readline().strip().split(',')

        try:
            assert "type" in headers
            assert "regex" in headers
            assert "desc" in headers
            assert "urgent" in headers
        except AssertionError:
            logging.error("CSV does not contain a proper header.")
            sys.exit()

        iType = headers.index("type")
        jsonFilters = {}
        for line in fin:
            line = line.strip().split(",")
            if len(line) != len(headers):
                logging.error("Missing column detected!")
                continue

            if line[iType] in jsonFilters:
                jsonFilters[line[iType]].append({"regex": line[headers.index("regex")],
                                                 "urgent": line[headers.index("urgent")],
                                                 "desc": line[headers.index("regex")]})
            else:
                jsonFilters[line[iType]] = [{"regex": line[headers.index("regex")],
                                             "urgent": line[headers.index("urgent")],
                                             "desc": line[headers.index("desc")]}]

    with open(filterFile, 'w') as fout:
        json.dump(jsonFilters, fout,
                  sort_keys=True,
                  indent=4,
                  separators=(',', ': '))


def main(args):

    if args.csv:
        loadCsv(args.csv, args.filters)
        return 0

    if args.add:
        updateJson(args.filters, args.ftype, args.regex, args.urgent, args.desc)
        return 0

    mainParser = phparsers.PhParser()
    digest = digestPaste.DigestPaste(args.filters)

    lastTime = time.time()
    reportTime = args.delayReport

    reports = []
    while not ev.isSet():
        ret = mainParser.run()

        if ret:
            for parser in ret:
                for paste in parser:
                    result = digest.digest(paste)
                    if result is not None:
                        reports.append(result)
                        result.save()

        currentTime = time.time()
        if currentTime - lastTime > reportTime:
            lastTime = currentTime
            if reports:
                sendReports(reports, args.phone, args.email)
                # for report in reports:
                #     print(report)
                reports = []

        digest.update()
        time.sleep(0.1)

    logging.info("bye!")

    return 0

if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_gracefully)
    ev = threading.Event()

    import arguments
    parser = arguments.getParser()

    sys.exit(main(parser.parse_args()))
