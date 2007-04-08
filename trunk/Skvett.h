/***************************************************************
 * Name:      Skvett.h
 * Purpose:   Dynamic vector
 * Author:    Luca Allulli (webmaster@roma21.it)
 * Created:   2007-03-25
 * Copyright: Luca Allulli (http://www.roma21.it/songpress)
 * License:   GNU GPL v2
 **************************************************************/
 
#ifndef SKVETT_H
#define SKVETT_H
#include<iostream.h>
#include<skCoda.h>

template<class E>
struct vettNodo {
	vettNodo* prev;
	E* val;
	vettNodo* next;
};

template <class E>
class skVett {
public:
	skVett();
	skVett(long);
	skVett(skVett<E>&);
	~skVett();
	skVett<E>& operator=(skVett<E>&);
	skVett<E>& ReDim(long);
	long DammiDim() {return dim;}
	E& operator[](long);
protected:
	long dim;	long actLo;	long actHi;	long actWdt;
	vettNodo<E>* act;
	long tmpLo;	long tmpHi;	long tmpWdt;
	vettNodo<E>* tmp;
	static void Copia(skVett&, skVett&);
	static void Distruggi(skVett&);
	void Sali();
	void Scendi();
	void SalvaTmp() {tmpLo=actLo;tmpHi=actHi;tmpWdt=actWdt;tmp=act;}
	void SaliTmp();
	void ScendiTmp();
};

template<class E>
class skVettO: public skVett<E> {
public:
	bool operator==(skVettO<E>&);
	bool operator>(skVettO<E>&);
	bool operator<(skVettO<E>&);
	bool operator>=(skVettO<E>&);
	bool operator<=(skVettO<E>&);
	bool operator!=(skVettO<E>&);
protected:
	void MaggUg(skVettO<E>&, bool& m, bool& u);
};

//class skVett
//public:
template<class E>
skVett<E>::skVett():dim(1),actLo(0),actHi(8),actWdt(8) {
	act=new vettNodo<E>;
	act->prev=act->next=NULL;
	act->val=new E[8];
}

template<class E>
skVett<E>::skVett(long b):dim(1),actLo(0) {
	if(b<1) b=8;
	act=new vettNodo<E>;
	act->prev=act->next=NULL;
	act->val=new E[b];
	actWdt=actHi=b; actLo=0;
}

template<class E>
skVett<E>::skVett(skVett<E>& v)
	{Copia(v,*this);}

template<class E>
skVett<E>::~skVett()
	{Distruggi(*this);}

template<class E>
skVett<E>& skVett<E>::operator=(skVett<E>& v) {
	if(&v!=this) {
		skVett<E> t;  //un vettore temporaneo...
		Distruggi(t);
		Copia(v,t);   //...su cui copia v...
		Distruggi(*this);
		act=t.act;actLo=t.actLo;actHi=t.actHi;actWdt=t.actWdt;dim=t.dim; //...da t a *this...
		skVett<E> r;  //...un vettore temporaneo...
		Copia(r,t);   //...che COPIA su t per poter DISTRUGGERE entrambi!
	}
	return *this;
}

template<class E>
skVett<E>& skVett<E>::ReDim(long d) {
	while(act->next!=NULL) Sali();
	while(d>actHi) {
		tmp=new vettNodo<E>;
		tmp->prev=act;
		tmp->next=NULL;
		tmp->val=new E[actWdt*2];
		act->next=tmp;
		Sali();
	}
	while(d<(actLo-actWdt/4)) {
		Scendi();
		delete[] act->next->val;
		delete act->next;
		act->next=NULL;
	}
	dim=d;
	return *this;
}

template<class E>
E& skVett<E>::operator[](long l) {
	while(l<actLo) Scendi();
	while(l>actHi-1) Sali();
	return act->val[l-actLo];
}

//private:

template<class E>
void skVett<E>::Sali() {
	act=act->next;
	actLo=actHi;
	actWdt=actWdt*2;
	actHi=actLo+actWdt;
}

template<class E>
void skVett<E>::Scendi() {
	act=act->prev;
	actHi=actLo;
	actWdt=actWdt/2;
	actLo=actHi-actWdt;
}

template<class E>
void skVett<E>::SaliTmp() {
	tmp=tmp->next;
	tmpLo=tmpHi;
	tmpWdt=tmpWdt*2;
	tmpHi=tmpLo+tmpWdt;
}

template<class E>
void skVett<E>::ScendiTmp() {
	tmp=tmp->prev;
	tmpHi=tmpLo;
	tmpWdt=tmpWdt/2;
	tmpLo=tmpHi-tmpWdt;
}

template<class E>
void skVett<E>::Copia(skVett<E>& s, skVett<E>& d) {
	long i;
	s.SalvaTmp();
	while(s.tmp->next!=NULL)
		s.SaliTmp();
	d.tmp=new vettNodo<E>;
	vettNodo<E>* v=d.tmp;
	vettNodo<E>* w;
	while(s.tmp!=NULL) {
		v->prev=new vettNodo<E>;
		w=v; v=v->prev;
		v->next=w;
		v->val=new E[s.tmpWdt];
		for(i=s.tmpWdt-1;i>=0;i--)
			v->val[i]=s.tmp->val[i];
		if(s.tmp==s.act)
		 d.act=v;
	s.ScendiTmp();
	}
	v->prev=NULL;
	v=d.tmp; d.tmp=v->prev; d.tmp->next=NULL; delete v;
	d.actLo=s.actLo; d.actHi=s.actHi; d.actWdt=s.actWdt; d.dim=s.dim;
}

template<class E>
void skVett<E>::Distruggi(skVett<E>& v) {
	vettNodo<E>* a;
	while(v.act->next!=NULL)
		v.act=v.act->next;
	while(v.act!=NULL) {
		a=v.act;
		delete[] a->val;
		v.act=a->prev;
		delete a;
	}
}

//class skVett
//public:
template<class E>
bool skVettO<E>::operator==(skVettO<E>& v) {
	bool m,u;
	MaggUg(v,m,u);
	return u;
}
template<class E>
bool skVettO<E>::operator>=(skVettO<E>& v) {
	bool m,u;
	MaggUg(v,m,u);
	return(m||u);
}
template<class E>
bool skVettO<E>::operator<=(skVettO<E>& v) {
	bool m,u;
	MaggUg(v,m,u);
	return(!m);
}
template<class E>
bool skVettO<E>::operator>(skVettO<E>& v) {
	bool m,u;
	MaggUg(v,m,u);
	return(m&&(!u));
}
template<class E>
bool skVettO<E>::operator<(skVettO<E>& v) {
	bool m,u;
	MaggUg(v,m,u);
	return((!m)&&(!u));
}
template<class E>
bool skVettO<E>::operator!=(skVettO<E>& v) {
	bool m,u;
	MaggUg(v,m,u);
	return(!u);
}


//protected:
template<class E>
void skVettO<E>::MaggUg(skVettO<E>& v, bool& m, bool& u) {
	long a=dim, b=v.dim;
	long i=0;
	while((i<a)&&(i<b)) {
		if((*this)[i]<v[i])
			{m=false; u=false; return;}
		else if((*this)[i]>v[i])
			{m=true; u=false; return;}
		i++;
	}
	if((i==a)&&(i==b))
		{m=false; u=true;}
	else if(i==a)
		{m=false; u=false;}
	else
		{m=true; u=false;}
}

#endif
