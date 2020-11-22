# dns_accuracy_and_performance
 
This is a relatively simple script that will resolve a DNS entry with multiple public DNS resolvers and perform an MTR to each ones primary A record result.
So it can be known which one is returning the 'best' result, an MTR is also performed to the primary IP of the resolver.
 
# Why?
dnsbench and other programs just test how quickly a result is returned, which isn't the full picture.
* A result may not be returned
* An inaccurate result may be returned for your location
* The path to your resolver is also important (number of hops / what networks its going through / general latency).

# TODO
- [ ] v6 support??
- [ ] Add more resolvers
- [ ] Add more CDNs tests
- [ ] Measure query time more accurately
- [ ] Print or save the mtr results
