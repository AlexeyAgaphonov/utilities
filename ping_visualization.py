# -*- coding: utf-8 -*-

import os
import sys
import ntpath
import re
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from pandas.core.frame import DataFrame

# Поддержка только при русских логах
# Для сбора логов с датой, используем:
# ping.exe -t {SERVER}|Foreach{"{0} - {1}" -f (Get-Date),$_} > {FILE}


def get_data(files) -> DataFrame:
    compiled_re = re.compile(r'([\d.]+ [\d:]+).*время=([\d]+)мс')
    datas = []
    for file_path in files:
        name = ntpath.basename(file_path)
        with open(file_path, 'r', encoding='utf-16') as f:
            for line in f:
                result = compiled_re.match(line)
                if result and len(result.groups()) > 1:
                    date = datetime.strptime(result.groups()[0], '%d.%m.%Y %H:%M:%S')
                    value = int(result.groups()[1])
                    datas.append([date, name, value])

    return DataFrame(datas, columns=['date', 'server', 'ping']).sort_values(by=['ping'])


if __name__ == '__main__':
    if len(sys.argv[1:]) > 0:
        full_data = get_data(sys.argv[1:])

        sns.lineplot(x="date", y="ping",
                     hue="server",
                     data=full_data)

        plt.show()
    else:
        print(u'[ERROR] Укажите хотя бы 1 файл с логами')