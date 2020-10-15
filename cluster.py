data = data.fillna('NULL')
    data['clean_sum'] = data[unstructure].apply(lambda x: cleanse_text(x))
    
    vectorizer = CountVectorizer(analyzer='word',stop_words='english',decode_error='ignore',binary=True)
    #vectorizer.fit(data[unstructure])    
    
    counts = vectorizer.fit_transform(data['clean_sum'])
    
    kmeans = KMeans(n_clusters=no_of_clusters,n_jobs=-1)
    
    data['cluster_num'] = kmeans.fit_predict(counts)
    data = data.drop(['clean_sum'],axis=1)
    output = StringIO.StringIO()
    data.to_csv(output,index=False)
    
    clusters = []
    for i in range(np.shape(kmeans.cluster_centers_)[0]):
        data_cluster = pd.concat([pd.Series(vectorizer.get_feature_names()),pd.DataFrame(kmeans.cluster_centers_[i])],axis=1)
        data_cluster.columns = ['keywords','weights']
        data_cluster = data_cluster.sort_values(by=['weights'],ascending=False)
        data_clust = data_cluster.head(n=10)['keywords'].tolist()
        clusters.append(data_clust)
        #print data_cluster.head(n=10)['keywords']
    #data_CLUSTERS.to_csv('output_full.csv',index=False)
    pd.DataFrame(clusters).to_csv('keywords_.csv')
    data.to_csv('Q2.csv',index=False)
   
   def index_guided():
    """
    This API will help you generate clusters based on keywords provided by you
    Call this api passing the following parameters - 
        Dataset - The data you want to cluster
        Column Name based on which clustering needs to be done
        Comma separated values of the keywords
    ---
    tags:
      - Clustering API
    parameters:
      - name: dataset
        in: formData
        type: file
        required: true
        description: The dataset
      - name: col
        in: query
        type: string
        required: true
        description: The column name based on which the clustering needs to be done
      - name: phrases
        in: formData
        type: file
        required: true
        description: The keywords for clustering in a single column in a csv
      
    """
    #file_ = request.args.get('upload')
    #print request.files
    data = pd.read_csv(request.files['dataset'])
    data_keywords = pd.read_csv(request.files['phrases'],header=None)
    #loc = request.args.get('dataset')
    #ext = loc.split('.')[-1]
    #ext='csv'
    #if 'ext' in request.args:
    #    ext = request.args.get('ext')
    
    unstructure = ''
    if 'col' in request.args:
        unstructure = request.args.get('col')
  
    data = data.fillna('NULL')
    data['clean_sum'] = data[unstructure].apply(lambda x: cleanse_text(x.lower()))
    #data.to_csv('clean_dat.csv',index=False)
    data_keywords = data_keywords.fillna('NULL')
    data_keywords[data_keywords.columns[0]] = data_keywords[data_keywords.columns[0]].apply(lambda x: str(x).lower())
    data_keywords['clean_keys'] = data_keywords[data_keywords.columns[0]].apply(lambda x: cleanse_text_guided(x))
    vocab_keys = data_keywords['clean_keys'].drop_duplicates().tolist()
    
    counts = np.zeros(shape=(np.shape(data)[0],len(vocab_keys)))
    data_counts = pd.DataFrame(counts,columns=vocab_keys)
    for phrase in vocab_keys:
        data_counts[phrase] = data['clean_sum'].apply(lambda x: phrase_in(x,phrase))
    data = data.drop(['clean_sum'],axis=1)
    data_output = pd.concat([data, data_counts], axis=1)
    output = StringIO.StringIO()
    data_output.to_csv(output,index=False)
 
