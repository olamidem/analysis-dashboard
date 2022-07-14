from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Pie,Bar
from .utilities import *


# Create your views here.
def index(request):
    import pandas as pd
    path = r'C:\Users\user\Desktop\state.csv'
    pd = pd.read_csv(path)
    converter(pd)
    pd['DaysOfARVRefill'] = pd['DaysOfARVRefill'].replace(to_replace=np.nan, value=0)
    pd['Outcomes'] = pd['Outcomes'].replace(to_replace=np.nan, value="")
    pd['IPT_Screening_Date'] = pd['IPT_Screening_Date'].replace(to_replace=np.nan, value="")
    plus = pd['DaysOfARVRefill'].astype(int)
    con = dateConverter(pd['LastPickupDateCal'])
    end = (con + plus.map(timedelta))
    treatment = tx_curr(pd)
    treatment_current_count = txCurr(treatment)
    male = maleTxCurr(treatment)
    female = femaleTxCurr(treatment)
    adult = adultTxCurr(treatment)
    adolescent = adolescentTxCurr(treatment)
    paediatrics = paedTxCurr(treatment)
    pbs_count = pbs(treatment)
    pbs_coverage = pbsCoverage(treatment)
    iptScreening_count = iptScreening(treatment)
    tbDocumented_result_count = documentedTb(treatment)
    newage = pd['New_Age']
    Current_TB_Status_count = CurrentTbStatus(treatment)
    tx_ml_count = tx_ml(treatment)
    returnToCare_count = returnToCare(treatment)

    pieChart = {'Name': ['RTT', 'TX_ML'],
                'values': [int(returnToCare_count), int(tx_ml_count)]}

    p = (
        Pie(init_opts=opts.InitOpts(width="500px", height="250px"))
            .add(
            "",
            [list(z) for z in zip(pieChart['Name'], pieChart['values'])],
            radius=["40%", "75%"],
        )
            .set_global_opts(
            legend_opts=opts.LegendOpts(orient="horizontal", is_show=False),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)", font_size=12)
                             )
    )
    age_group = treatment.query('Sex == "M" ')
    fiftyplus, lessthanforty_four, lessthanforty_nine, lessthanfour, lessthanfourteen, \
    lessthannineteen, lessthanone, lessthanten, lessthanthirty_four, lessthanthirty_nine, \
    lessthantwenty_four, lessthantwenty_nine = age_grouping(
        age_group)

    male_male = [lessthanone, lessthanfour, lessthanten, lessthanfourteen,
            lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
            lessthanthirty_four, lessthanthirty_nine, lessthanforty_four,
            lessthanforty_nine, fiftyplus]

    age_group_female = treatment.query('Sex == "F" ')
    fiftyplus, lessthanforty_four, lessthanforty_nine, lessthanfour, lessthanfourteen, \
    lessthannineteen, lessthanone, lessthanten, lessthanthirty_four, lessthanthirty_nine, \
    lessthantwenty_four, lessthantwenty_nine = age_grouping(
        age_group_female)

    female_female = [lessthanone, lessthanfour, lessthanten, lessthanfourteen,
              lessthannineteen, lessthantwenty_four, lessthantwenty_nine,
              lessthanthirty_four, lessthanthirty_nine, lessthanforty_four, lessthanforty_nine,
              fiftyplus]

    female_female = [int(i) for i in female_female]
    male_male = [int(i) for i in male_male]

    bar_chart_display(female_female, female_female)

    return render(request, 'app/index.html', {
        'pd': pd,
        'treatment_current_count': treatment_current_count,
        'male': male,
        'female': female,
        'adult': adult,
        'adolescent': adolescent,
        'paediatrics': paediatrics,
        'pbs_count': pbs_count,
        'pbs_coverage': pbs_coverage,
        'iptScreening_count': iptScreening_count,
        'tbDocumented_result_count': tbDocumented_result_count,
        'newage': newage,
        'Current_TB_Status_count': Current_TB_Status_count,
        'tx_ml_count': tx_ml_count,
        'returnToCare_count': returnToCare_count,
        'pieChart': p.render_embed(),
        'bar_chart': bar_chart_display(male_male,female_female).render_embed()

    })
