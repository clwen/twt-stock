from scipy.stats.stats import pearsonr

companies = ['apple', 'google', 'microsoft', 'amazon', 'rim', 'dell', 'intel', 'yahoo', 'nvidia', 'netflix']

def extract_ratios(company):
    ratios = []
    ratio_file = 'outputs/' + company
    lines = open(ratio_file, 'r').readlines()
    for line in lines:
        tokens = line.split()
        ratios.append(float(tokens[0]))
    return ratios

def extract_prices(company):
    week_num = 7 # number of weeks to parse
    prices = []
    price_file = 'stock-prices/' + company + '.csv'
    lines = open(price_file, 'r').readlines()
    lines = lines[2:2+week_num] # ignore first line, which is header
    for line in lines:
        tokens = line.split(',')
        prices.append(float(tokens[4]))
    return prices

if __name__ == '__main__':
    pearsons = []
    for company in companies:
        output_path = 'pearsons/' + company
        # of = open(output_path, 'w')

        ratios = extract_ratios(company)
        prices = extract_prices(company)
        (pearson, pvalue) = pearsonr(ratios, prices)
        pearsons.append(pearson)
        output_line = "%s & %s & %s \\\\ \hline\n" % (company, pearson, pvalue)
        print output_line,
        # print '\t' + str(ratios)
        # print '\t' + str(prices)
        # of.write(str(pearson) + '\n')
        # of.write(str(ratios) + '\n')
        # of.write(str(prices) + '\n')
    pearsons_avg = sum(pearsons) / len(pearsons)
    print pearsons_avg

