# import Flask
from flask import Flask, render_template, redirect, jsonify
from read_data import session, OTU, Sample, Sample_Meta

# initialize flask app
app = Flask(__name__)

# retun dashboard homepage
@app.route('/')
def index():
    return render_template('index.html')

# return list of sample names
@app.route('/names')
def names():
    # query db for sample names
    sample_names = Sample.__table__.columns._data.keys()[1:]
    return jsonify(sample_names)

# return list of OTU descriptions
@app.route('/otu')
def otu():
    # query db otu descriptions
    otu_query = session.query(OTU)
    # convert to list of values rather than list of tuples
    otu_recs = {otu.otu_id: otu.lowest_taxonomic_unit_found for otu in otu_query}
    return jsonify(otu_recs)

# return metadata for a given sample
@app.route('/metadata/<sample>')
def metadata(sample):
    # remove prefix from sample name
    sample_value = sample.lstrip('BB_')
    
    meta_dict = {}
    # query db and filter for given sample
    meta_query = (session
                .query(Sample_Meta)
                .filter(Sample_Meta.SAMPLEID == sample_value))

    for record in meta_query:
        meta_dict = {
            'AGE': record.AGE,
            'BBTYPE': record.BBTYPE,
            'ETHNICITY': record.ETHNICITY,
            'GENDER': record.GENDER,
            'LOCATION': record.LOCATION,
            'SAMPLEID': record.SAMPLEID,
        }

    return jsonify(meta_dict)

# return wekly washing frequency for a given sample
@app.route('/wfreq/<sample>')
def wfreq(sample):
    # remove prefix from sample name
    sample_value = sample.lstrip('BB_')
    
    # query db for wfreq and return as scalar
    wfreq_query = (session
            .query(Sample_Meta.WFREQ)
            .filter(Sample_Meta.SAMPLEID == sample_value)
            .scalar())

    return jsonify(wfreq_query)

# return OTU ID and sample values for given sample
@app.route('/sample/<sample>')
def sample(sample):
    # query db for sample value and otu_id
    sample_query = session.query(Sample.otu_id, getattr(Sample, sample))

    # sort sample values in descending order
    sample_query_sorted = sorted(sample_query, key=lambda x: x[1], reverse=True)

    # create dict with lists of ids and sample values  
    sample_dict = {
        'otu_ids': [otu[0] for otu in sample_query_sorted],
        'sample_values': [otu[1] for otu in sample_query_sorted]
    }

    return jsonify(sample_dict)

if __name__ == '__main__':
    app.run(debug=True)