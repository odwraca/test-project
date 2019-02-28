import boto3
from datetime import datetime 
import os
import time
import json
import urllib.parse

response = """Return-Path: <odwraca@gmail.com>
Received: from mail-qt1-f182.google.com (mail-qt1-f182.google.com [209.85.160.182])
 by inbound-smtp.us-east-1.amazonaws.com with SMTP id 1ld45m5nepdsqavklntitktv5b5ps6ge9ep207g1
 for hogtrap+01@traps.curtisbroscattle.com;
 Wed, 20 Feb 2019 17:06:19 +0000 (UTC)
X-SES-Spam-Verdict: PASS
X-SES-Virus-Verdict: PASS
Received-SPF: pass (spfCheck: domain of _spf.google.com designates 209.85.160.182 as permitted sender) client-ip=209.85.160.182; envelope-from=odwraca@gmail.com; helo=mail-qt1-f182.google.com;
Authentication-Results: amazonses.com;
 spf=pass (spfCheck: domain of _spf.google.com designates 209.85.160.182 as permitted sender) client-ip=209.85.160.182; envelope-from=odwraca@gmail.com; helo=mail-qt1-f182.google.com;
 dkim=pass header.i=@gmail.com;
 dmarc=pass header.from=gmail.com;
X-SES-RECEIPT: AEFBQUFBQUFBQUFHajE4Z2NMVTV5a01RYjg3dVpuOWtqZ1VPOXg5N2RPOW5SZlVjUTZ3UlNVekxpQU1kVllOMlhEdEhmSEtHZ1VZQmZZZERJN2JRaGwrL0Z6VjVhUjdwZVNMS0FwK3FQeTE5T2VTZlF3Vk0yZ0tFZmcyb3RKbzNBY3dFbDA2Um9icTV4NGQ5Qk5lZm8wZzI4YUNIdlVMU01iaTVEWTNLdUNJSEs2WE5Vd0FSUG5lYmxoaGpDcGxOSDdwU21jeEtwbExVNmpqdEcwVUFkNXlkbzJiazZ2ZzFyeDlIaG1xOHNVMzlRT3Rzb1BlNEwrQlhmeFlSSDdIMklBMWREaVpBc0ZYdkFKcDJGRmo5cnM0Y0s3YkltTytjVnFMcDZSdkZ4aHF2RkR4SmNDSnk2VWc9PQ==
X-SES-DKIM-SIGNATURE: a=rsa-sha256; q=dns/txt; b=RttSeT+cteA7pGOSEepmH3LAsa02kBcWhjHlwy6AKQZ8cT3hmSGu0IbYGTz9GFPHL4+NeZ8Q2kOpiaLYPrBhIm+Li5ZPwP8aXiSF0is9jue+GcUto8X5vwANJpd1qD+wC9h3m9FUzDZVjP330zozW4fk6/Q5ApkmpQj5GFgSxEU=; c=relaxed/simple; s=ug7nbtf4gccmlpwj322ax3p6ow6yfsug; d=amazonses.com; t=1550682379; v=1; bh=J5NjxwpN+bosiH5Tv4oZd24jq46hbeQ0OuT2VPZwAXM=; h=From:To:Cc:Bcc:Subject:Date:Message-ID:MIME-Version:Content-Type:X-SES-RECEIPT;
Received: by mail-qt1-f182.google.com with SMTP id o6so27997803qtk.6
        for <hogtrap+01@traps.curtisbroscattle.com>; Wed, 20 Feb 2019 09:06:19 -0800 (PST)
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=gmail.com; s=20161025;
        h=mime-version:from:date:message-id:subject:to;
        bh=grvaQVnwGOxWSwddmQ1EXXPBaf/49tLgyQRLjtR7Dkw=;
        b=X4Ed9RSs5q8o9o61QR7YQmhqkIsrO0DQIabx6WiFOPYbmXfR4jz/gL7Ixs37MUIogP
         Y6qLfmRmLFmxbwuSCBNgdjr/Ua5XlpVtcoO9O4ghMvEP7U1/Fsrke2nBBKywsuBQwi66
         jLxP+TOfxlECgA8x22586+CGa8wC7XcEDkVeaLn5IDkxV5UPGlhRk6yUYvaKXPrySEbE
         W0BOMdnXXcHj5mWLrrKyKuocshS79Ux4bYRxggEu/7GJZ5zyRXSvHQ7SFnarWyxG7OSz
         n6Nvzatyov6gaInZRh/7qz7FVVPiuc+RC9Sa7byIVmvDJ9X0E4ZXpGjjmRbrICMBfKmc
         lkJQ==
X-Google-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=1e100.net; s=20161025;
        h=x-gm-message-state:mime-version:from:date:message-id:subject:to;
        bh=grvaQVnwGOxWSwddmQ1EXXPBaf/49tLgyQRLjtR7Dkw=;
        b=e1FbN/s/q907rf2K3iDuZezneAlyhNTVSSiY098qZQOYKWQ8L+H4T9BaZAMNENdPKC
         wubY/JSgh+foSPe/2QOZjSKlF7MZaM5M+cRDMtdLeRK73alBUjFErHKC5PwYhsap0oNo
         BTCg4jHVUAJfCPQBT2/JZtsvguLFqDOUhDhpbvVigwVCoKJTwjgtA8UfD5/h64+hqycp
         O8dJUQMThA2+/mF7TdQp5HRtQmQVLGV2jfYFQG/me9krcCMJQJCP5Po49X5JBGs7uw93
         IpnS5aTvHR8r9JLQctNNnjZoHFZe/N/8EwR1mZLNN7dTe9BGg5Rfqbypm+HOKEoOrGwa
         oynA==
X-Gm-Message-State: AHQUAuad71nDQZVjwlp2h6CUjZl3sj1e34Fn8ocmFEnPOhNNnyZivMQf
        S7lQIrPw5e1sl6MczHNKkBhl56dX+0nyBf43M40ATV1L
X-Google-Smtp-Source: AHgI3IbWoGvHlgsR9yR44ahmTJyrUS5TCvnvZEKY9gFFv1xv0bFqfEfZ5c8uVQyWeZe92jKmzQCVt5JsEnjw9dWrek8=
X-Received: by 2002:ac8:1015:: with SMTP id z21mr551212qti.102.1550682378894;
 Wed, 20 Feb 2019 09:06:18 -0800 (PST)
MIME-Version: 1.0
From: Odwraca <odwraca@gmail.com>
Date: Wed, 20 Feb 2019 11:06:05 -0600
Message-ID: <CA+bwJqVbCqDx5EYua13Yi1b6ykdQv7OWAqRBKPKqOqpBbA-NFw@mail.gmail.com>
Subject: Test email 1105a
To: hogtrap+01@traps.curtisbroscattle.com
Content-Type: multipart/alternative; boundary="0000000000005a83fc0582566039"

--0000000000005a83fc0582566039
Content-Type: text/plain; charset="UTF-8"

motion detected

-- 
*Aaron Curtis*
C: 903-563-5684

--0000000000005a83fc0582566039
Content-Type: text/html; charset="UTF-8"
Content-Transfer-Encoding: quoted-printable

<div dir=3D"ltr">motion detected<br clear=3D"all"><div><br></div>-- <br><di=
v dir=3D"ltr" class=3D"gmail_signature" data-smartmail=3D"gmail_signature">=
<div dir=3D"ltr"><div><div dir=3D"ltr"><div><b>Aaron Curtis</b></div><div>C=
: 903-563-5684</div></div></div></div></div></div>

--0000000000005a83fc0582566039--
"""
file_path = "/Users/aaarcr/Downloads/out.txt"
email_content = response
email_lines = email_content.splitlines()
for line in range(len(email_lines)):
        email_info = {}
        if "Date" in email_lines[line]:
                email_info['Date'] = email_lines[line][6:]
                email_info['Subject'] = email_lines[line+2][9:]
                #email_info['From'] = email_lines[line+12][6:]
                email_info['To'] = email_lines[line+3][4:]
                with open(file_path, 'w') as outfile:
                        json.dump(email_info, outfile)
# Upload to S3.
#s3.upload_file(file_path, s3_folder, file_name)
#print("Upload Successful")

