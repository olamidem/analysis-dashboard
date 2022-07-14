import pandas as pd
from datetime import timedelta, date, datetime
from pyecharts import options as opts
from pyecharts.charts import Pie, Bar


def dateConverter(dateColumn):
    return pd.to_datetime(dateColumn, format="%d/%m/%Y", errors='ignore')


def tx_curr(dataSet):
    return dataSet.query(
        'CurrentARTStatus_Pharmacy == "Active" & Outcomes == ""  ')


def txCurr(treatmentCurrent):
    treatmentCurrent_count = treatmentCurrent['CurrentARTStatus_Pharmacy'].count()
    treatmentCurrent_count = f'{treatmentCurrent_count:,d}'
    return treatmentCurrent_count


def maleTxCurr(treatmentCurrent):
    tx_curr_male = treatmentCurrent.query('Sex == "M" ')
    countMale = tx_curr_male['Sex'].count()
    male = f'{countMale:,d}'
    return male


def paedTxCurr(treatmentCurrent):
    paed = treatmentCurrent.query('New_Age <10 ')
    countPaed = paed['New_Age'].count()
    countAdolescent = f'{countPaed:,d}'
    return countAdolescent


def adolescentTxCurr(treatmentCurrent):
    adolescent = treatmentCurrent.query('New_Age >=10 & New_Age <= 19 ')
    countAdolescent = adolescent['New_Age'].count()
    countAdolescent = f'{countAdolescent:,d}'
    return countAdolescent


def adultTxCurr(treatmentCurrent):
    adult = treatmentCurrent.query('New_Age >= 20 ')
    countAdult = adult['New_Age'].count()
    countAdult = f'{countAdult:,d}'
    return countAdult


def femaleTxCurr(treatmentCurrent):
    tx_curr_female = treatmentCurrent.query('Sex == "F" ')
    countFemale = tx_curr_female['Sex'].count()
    female = f'{countFemale:,d}'
    return female


def pbs(treatmentCurrent):
    pbs_check = treatmentCurrent.query('PBS == "Yes" ')
    pbs_count = pbs_check['PBS'].count()
    pbs_count = f'{pbs_count:,d}'
    return pbs_count


def pbsCoverage(treatmentCurrent):
    tx = treatmentCurrent.query('CurrentARTStatus_Pharmacy == "Active" & Outcomes == ""  ')
    pbs_query = treatmentCurrent.query('PBS == "Yes" ')
    tx_count = tx['CurrentARTStatus_Pharmacy'].count()
    pbs_count = pbs_query['PBS'].count()
    pbs_coverage_count = ((pbs_count / tx_count) * 100).round(1)
    return pbs_coverage_count


def iptScreening(treatmentCurrent):
    ipt_screening_query = treatmentCurrent.query('IPT_Screening_Date != "" ')
    ipt_screening_count = ipt_screening_query['IPT_Screening_Date'].count()
    ipt_screening_count = f'{ipt_screening_count:,d}'
    return ipt_screening_count


def tbDocumentedResults(treatmentCurrent):
    return treatmentCurrent.query('Sputum_AFB_Result == "Positive" | '
                                  'Sputum_AFB_Result == "Negative" | '
                                  'GeneXpert_Result == "Smear negative pulmonary '
                                  'tuberculosis patient" | GeneXpert_Result == "MTB '
                                  'not Detected" | GeneXpert_Result == "MTB '
                                  'Detected" | Chest_Xray_Result == "Suggestive" | '
                                  'Chest_Xray_Result == "Not Suggestive" | '
                                  'Culture_Result == "Posive" | Culture_Result == '
                                  '"Negative" ')


def documentedTb(treatmentCurrent):
    tbDocumented_result = tbDocumentedResults(treatmentCurrent)
    tbDocumented_result_count = tbDocumented_result['State'].count()
    tbDocumented_result_count = f'{tbDocumented_result_count:,d}'
    return tbDocumented_result_count


def CurrentTbStatus(treatmentCurrent):
    Current_TB_Status = treatmentCurrent.query(
        'Current_TB_Status == "Disease suspected" | Current_TB_Status '
        '== "On treatment for disease" | Current_TB_Status == '
        ' "Disease diagnosed"')
    Current_TB_Status_count = Current_TB_Status['Current_TB_Status'].count()
    Current_TB_Status_count = f'{Current_TB_Status_count:,d}'
    return Current_TB_Status_count


def converter(df):
    dob = dateConverter(df['DOB'])
    dob = dob.dt.date
    saveDate = date.today()
    df['today_date'] = saveDate
    df['New_Age'] = (saveDate - dob) / 365
    df['New_Age'] = df['New_Age'].dt.days


def tx_ml(treatmentCurrent):
    txML = treatmentCurrent.query('ARTStatus_PreviousQuarter == "Active" & CurrentARTStatus_Pharmacy != "Active"  ')
    txML_count = txML['ARTStatus_PreviousQuarter'].count()
    # txML_count = f'{txML_count:,d}'
    return txML_count


def returnToCare(treatmentCurrent):
    rtt = treatmentCurrent.query('ARTStatus_PreviousQuarter != "Active" & CurrentARTStatus_Pharmacy == "Active"  ')
    rtt_count = rtt['ARTStatus_PreviousQuarter'].count()
    # rtt_count = f'{rtt_count:,d}'
    return rtt_count


def age_grouping(age_group):
    lessthanone = age_group.query('New_Age < 1')
    lessthanone = lessthanone['New_Age'].count()
    lessthanfour = age_group.query('New_Age > = 1 & New_Age <= 4 ')
    lessthanfour = lessthanfour['New_Age'].count()
    lessthanten = age_group.query(' New_Age > = 5 & New_Age <= 9 ')
    lessthanten = lessthanten['New_Age'].count()
    lessthanfourteen = age_group.query('New_Age > = 10 & New_Age <= 14 ')
    lessthanfourteen = lessthanfourteen['New_Age'].count()
    lessthannineteen = age_group.query(' New_Age > = 15 & New_Age <= 19 ')
    lessthannineteen = lessthannineteen['New_Age'].count()
    lessthantwenty_four = age_group.query(' New_Age > = 20 & New_Age <= 24 ')
    lessthantwenty_four = lessthantwenty_four['New_Age'].count()
    lessthantwenty_nine = age_group.query('  New_Age > = 25 & New_Age <= 29 ')
    lessthantwenty_nine = lessthantwenty_nine['New_Age'].count()
    lessthanthirty_four = age_group.query(' New_Age > = 30 & New_Age <= 34 ')
    lessthanthirty_four = lessthanthirty_four['New_Age'].count()
    lessthanthirty_nine = age_group.query('New_Age > = 35 & New_Age <= 39 ')
    lessthanthirty_nine = lessthanthirty_nine['New_Age'].count()
    lessthanforty_four = age_group.query(' New_Age > = 40 & New_Age <= 44 ')
    lessthanforty_four = lessthanforty_four['New_Age'].count()
    lessthanforty_nine = age_group.query(' New_Age > = 45 & New_Age <= 49 ')
    lessthanforty_nine = lessthanforty_nine['New_Age'].count()
    fiftyplus = age_group.query(' New_Age  >= 50 ')
    fiftyplus = fiftyplus['New_Age'].count()
    return fiftyplus, lessthanforty_four, lessthanforty_nine, lessthanfour, lessthanfourteen, lessthannineteen, lessthanone, lessthanten, lessthanthirty_four, lessthanthirty_nine, lessthantwenty_four, lessthantwenty_nine


def pregnant_grouping(age_group):
    lessthannineteen = age_group.query(' Current_Age > = 15 & Current_Age <= 19 ')
    lessthannineteen = lessthannineteen['Current_Age'].count()
    lessthantwenty_four = age_group.query(' Current_Age > = 20 & Current_Age <= 24 ')
    lessthantwenty_four = lessthantwenty_four['Current_Age'].count()
    lessthantwenty_nine = age_group.query('  Current_Age > = 25 & Current_Age <= 29 ')
    lessthantwenty_nine = lessthantwenty_nine['Current_Age'].count()
    lessthanthirty_four = age_group.query(' Current_Age > = 30 & Current_Age <= 34 ')
    lessthanthirty_four = lessthanthirty_four['Current_Age'].count()
    lessthanthirty_nine = age_group.query('Current_Age > = 35 & Current_Age <= 39 ')
    lessthanthirty_nine = lessthanthirty_nine['Current_Age'].count()
    lessthanforty_four = age_group.query(' Current_Age > = 40 & Current_Age <= 44 ')
    lessthanforty_four = lessthanforty_four['Current_Age'].count()
    lessthanforty_nine = age_group.query(' Current_Age > = 45 & Current_Age <= 49 ')
    lessthanforty_nine = lessthanforty_nine['Current_Age'].count()
    fiftyplus = age_group.query(' Current_Age  >= 50 ')
    fiftyplus = fiftyplus['Current_Age'].count()
    return fiftyplus, lessthanforty_four, lessthanforty_nine, lessthannineteen, lessthanthirty_four, lessthanthirty_nine, lessthantwenty_four, lessthantwenty_nine


def bar_chart_display(female, male):
    age_disaggregation = ['<1', '1-4', '5-9', '10-14',
                          '15-19', '20-24', '25-29',
                          '30-34', '35-39', '40-44', '45-49', '50+']
    c = (
        Bar()
            .add_xaxis(age_disaggregation)
            .add_yaxis("MALE", male, gap="15%")
            .add_yaxis("FEMALE", female, gap="15%")
            .extend_axis(
            # yaxis=opts.AxisOpts(
            #     name="Percentage %",
            #     type_="value",
            #     min_=0,
            #     max_=100,
            #     position="right",
            #     axisline_opts=opts.AxisLineOpts(
            #         linestyle_opts=opts.LineStyleOpts(color="green")
            #     ),
            #     axislabel_opts=opts.LabelOpts(formatter="{value} %"),
            #     splitline_opts=opts.SplitLineOpts(
            #         is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
            #     ),
            # )
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="Sex and Age Group", subtitle="CURRENT AGE"))

    )
    return c
