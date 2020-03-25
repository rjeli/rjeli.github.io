---
layout: post
title: 'C++ Competition Reference'
---

This post will cover basic I/O and data structures for use in programming competitions.

C++ is an incredibly complex language, but you can be productive and solve constrained problems by ignoring 99% of the language and using the STL.

C++ is the best choice for programming competitions. It is much faster than Java, and if you study well, you will find it is not much more difficult to write than Java.

Make sure the competition you are attending has enabled C++11 compilation.

You can include all STL headers at once by including <bits/stdc++.h>. So, your skeleton program will look something like the following.

{% highlight cpp %}
#include <bits/stdc++.h>
using namespace std;

int
main(void)
{
	return 0;
}
{% endhighlight %}

# Input

If input is given as a file argument:

{% highlight cpp %}
int
main(int argc, char **argv)
{
	ifstream fin(argv[1]);
	while (!fin.eof()) {
	      fin >> // ...
	}
	
	return 0;
}
{% endhighlight %}

But, usually you can just read from STDIN.

{% highlight cpp %}
int
main(void)
{
	int n;
	cin >> n;
	for (int i=0; i<n; ++i) {
		cin >> // ...
	}
	
	return 0;
}
{% endhighlight %}

# Vectors

{% highlight cpp %}
vector<int> xs;
xs.resize(n);
xs.resize(n, 0);
{% endhighlight %}

If it becomes a smaller size, the extra values are destroyed. If it becomes a larger size, either the extra cells will be filled with the provided argument, or in its absence,	with the default constructor of the type. Primitive types such as int will be filled with garbage.

# Iteration:

{% highlight cpp %}
// By value, i.e. immutable
for (auto x : xs)
	cout << x;

// By reference, i.e. mutable
for (auto& x : xs)
	x = 1;
{% endhighlight %}

Stack operations:

{% highlight cpp %}
// Push
xs.push_back(100);

// Peek/Pop
int x = xs.back()
xs.pop_back();

// Flush
while (!xs.empty()) {
	cout << xs.back();
	xs.pop_back();
}
{% endhighlight %}

Note that these stack operations are efficient and will not cause too much reallocation because vector maintains a reserved amount of memory.

Convenient methods:

{% highlight cpp %}
xs.size() // number of elements
xs.clear() // same as xs.resize(0)
{% endhighlight %}

# Sets

{% highlight cpp %}
unordered_set<string> s;
s.insert("foo");
s.insert("bar");
{% endhighlight %}

Test for membership by searching for the element.

{% highlight cpp %}
string el = s.find("foo");
if (el == s.end())
	// el not in s
else
	// el in s
{% endhighlight %}

Remove by erasing the obtained iterator.

{% highlight cpp %}
s.erase(el);
{% endhighlight %}

Convenient methods:

{% highlight cpp %}
s.count(); // number of items
s.clear(); // erase all items
{% endhighlight %}

Iteration is identical to the vector.

# Hash Maps

{% highlight cpp %}
unordered_map<string,int> m;
m["foo"] = 1;
m["bar"] = 2;
{% endhighlight %}

Iteration:

{% highlight cpp %}
for (auto& x : m)
	cout << x.first << ": " << x.second << endl;
{% endhighlight %}

# Transformations

I recommend defining a macro to make working with collections easier.

{% highlight cpp %}
#define ALL(c) c.begin(),c.end()
{% endhighlight %}

Here is the example collection:

{% highlight cpp %}
vector<int> xs = { 1, 2, 3, 4, 5 };
{% endhighlight %}

### Sort

{% highlight cpp %}
sort(xs);
{% endhighlight %}

### Map

{% highlight cpp %}
transform(ALL(xs), xs.begin(), [](int x){
	return x+1;
});
{% endhighlight %}

### Filter

{% highlight cpp %}
auto is_odd = [](int x){ return x%2; };
remove_if(ALL(xs), is_odd);
{% endhighlight %}

### Reduce

{% highlight cpp %}
auto sum_reducer = [](double a, double b){
	return a + b;
});
accumulate(ALL(xs), 0.0, sum_reducer);
{% endhighlight %}

### Predicates

{% highlight cpp %}
bool all_odd = all_of(ALL(xs), is_odd);
bool any_odd = any_of(ALL(xs), is_odd);
bool none_odd = none_of(ALL(xs), is_odd);
{% endhighlight %}

### Permutations

This is extremely useful for bruteforcing. Make sure the collection is sorted beforehand.

{% highlight cpp %}
do {
	for (auto x : xs) cout << x;
	cout << endl;
} while (next_permutation(ALL(xs)));
{% endhighlight %}

### Set operations

You can use these on vectors as well, but be sure to sort them beforehand.

{% highlight cpp %}
unordered_set<int> s1, s2, res;
set_difference(ALL(s1), ALL(s2), inserter(res, res.end()));
set_intersection(ALL(s1), ALL(s2), inserter(res, res.end()));
set_union(ALL(s1), ALL(s2), inserter(res, res.end()));
{% endhighlight %}

