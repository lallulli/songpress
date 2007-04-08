/***************************************************************
 * Name:      Skcoda.h
 * Purpose:   Generic queue
 * Author:    Luca Allulli (webmaster@roma21.it)
 * Created:   2007-03-25
 * Copyright: Luca Allulli (http://www.roma21.it/songpress)
 * License:   GNU GPL v2
 **************************************************************/

#ifndef SKCODA_H
#define SKCODA_H
//#include <iostream.h>

template<class E>
struct skCodaRec {
	E val;
	skCodaRec<E>* next;
};

template<class E>
struct skCodaRapp {
	skCodaRec<E>* iniz;
	skCodaRec<E>* fine;
	long dim;
};

template<class E>
class skCoda {
public:
	skCoda() {r.iniz=r.fine=NULL; r.dim=0;}
	skCoda(const skCoda<E>& c) {r=Copia(c.r);}
	~skCoda() {Distruggi(r);}
	skCoda& operator=(const skCoda<E>&);
	long DammiDimensione() {return r.dim;}
	bool EstVuota() {return r.dim==0;}
	skCoda& InCoda(E);
	E OutCoda();
private:
	skCodaRapp<E> r;
	skCodaRapp<E> Copia(skCodaRapp<E>);
	void Distruggi(skCodaRapp<E>);
};

template<class E>
skCoda<E>& skCoda<E>::operator=(const skCoda<E>& c) {
	if (this!=&c) {
		skCodaRapp<E> s=Copia(c.r);
		Distruggi(r);
		r=s;
	}
	return *this;
}

template<class E>
skCoda<E>& skCoda<E>::InCoda(E e) {
	r.dim++;
	if(r.dim==1) {
		r.iniz=r.fine=new skCodaRec<E>;
		r.iniz->val=e;
		r.iniz->next=NULL;
	} else {
		r.fine->next=new skCodaRec<E>;
		r.fine=r.fine->next;
		r.fine->val=e;
		r.fine->next=NULL;
	}
	return *this;
}

template<class E>
E skCoda<E>::OutCoda() {
	r.dim--;
	E e=r.iniz->val;
	skCodaRec<E>* t=r.iniz;
	r.iniz=r.iniz->next;
	delete t;
	if(r.dim==0) r.fine=NULL;
	return e;
}

//private:
template <class E>
skCodaRapp<E> skCoda<E>::Copia(skCodaRapp<E> r) {
	if(r.dim!=0) {
		skCodaRec<E>* t=new skCodaRec<E>;
		skCodaRec<E>* s=t;
		while(r.iniz!=NULL) {
			t->next=new skCodaRec<E>;
			t=t->next;
			t->val=r.iniz->val;
			r.iniz=r.iniz->next;
		}
		t->next=NULL;
		r.fine=t;
		r.iniz=s->next;
		delete s;
	}
	return r;
}

template<class E>
void skCoda<E>::Distruggi(skCodaRapp<E> r) {
	skCodaRec<E>* t;
	while(r.iniz!=NULL)
		{t=r.iniz; r.iniz=t->next; delete t;}
}

#endif
