"use client";

import React, { useState, useEffect } from 'react';
import { clientApi } from '../lib/api';
import { Client, ClientCreate } from '../lib/types';

const HomePage: React.FC = () => {
  const [clients, setClients] = useState<Client[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showAddClientModal, setShowAddClientModal] = useState(false);
  const [newClientData, setNewClientData] = useState<ClientCreate>({
    name: '',
    email: '',
    phone: '',
    type: 'pme',
    activity_sector: '',
    address: '',
    notes: '',
  });

  const fetchClients = async () => {
    try {
      setIsLoading(true);
      const data = await clientApi.list();
      setClients(data);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch clients.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchClients();
  }, []);

  const handleNewClientChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setNewClientData(prev => ({ ...prev, [name]: value }));
  };

  const handleAddClientSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await clientApi.create(newClientData);
      setShowAddClientModal(false);
      setNewClientData({ name: '', email: '', phone: '', type: 'pme', activity_sector: '', address: '', notes: '' });
      fetchClients(); // Refresh client list
    } catch (err: any) {
      setError(err.message || 'Failed to add new client.');
    }
  };

  if (isLoading) return <div className="flex justify-center items-center h-screen bg-gray-100">Chargement des clients...</div>;
  if (error) return <div className="flex justify-center items-center h-screen bg-red-100 text-red-700">Erreur: {error}</div>;

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Clients CRM IA</h1>
        
        <div className="flex justify-end mb-6">
          <button 
            onClick={() => setShowAddClientModal(true)}
            className="btn-primary"
          >
            + Ajouter un Client
          </button>
        </div>

        {clients.length === 0 ? (
          <p className="text-gray-600 text-center">Aucun client trouvé. Ajoutez votre premier client !</p>
        ) : (
          <div className="card">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nom</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Téléphone</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Secteur</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Dossiers</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {clients.map(client => (
                    <tr key={client.id}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{client.name}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{client.email}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{client.phone}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{client.type}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{client.activity_sector}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{client.cases_count}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <a href={`/clients/${client.id}`} className="text-indigo-600 hover:text-indigo-900 mr-4">Voir</a>
                        <button className="text-red-600 hover:text-red-900">Supprimer</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      {showAddClientModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center">
          <div className="bg-white p-8 rounded-lg shadow-xl max-w-md mx-auto">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Ajouter un Nouveau Client</h2>
            <form onSubmit={handleAddClientSubmit} className="space-y-4">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700">Nom Complet</label>
                <input type="text" name="name" id="name" value={newClientData.name} onChange={handleNewClientChange} className="input-field" required />
              </div>
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
                <input type="email" name="email" id="email" value={newClientData.email} onChange={handleNewClientChange} className="input-field" />
              </div>
              <div>
                <label htmlFor="phone" className="block text-sm font-medium text-gray-700">Téléphone</label>
                <input type="text" name="phone" id="phone" value={newClientData.phone} onChange={handleNewClientChange} className="input-field" />
              </div>
              <div>
                <label htmlFor="type" className="block text-sm font-medium text-gray-700">Type de Client</label>
                <select name="type" id="type" value={newClientData.type} onChange={handleNewClientChange} className="input-field">
                  <option value="pme">PME</option>
                  <option value="freelance">Freelance</option>
                  <option value="particulier">Particulier</option>
                  <option value="entreprise">Entreprise</option>
                  <option value="cabinet">Cabinet</option>
                </select>
              </div>
              <div>
                <label htmlFor="activity_sector" className="block text-sm font-medium text-gray-700">Secteur d'Activité</label>
                <input type="text" name="activity_sector" id="activity_sector" value={newClientData.activity_sector} onChange={handleNewClientChange} className="input-field" />
              </div>
              <div>
                <label htmlFor="address" className="block text-sm font-medium text-gray-700">Adresse</label>
                <input type="text" name="address" id="address" value={newClientData.address} onChange={handleNewClientChange} className="input-field" />
              </div>
              <div>
                <label htmlFor="notes" className="block text-sm font-medium text-gray-700">Notes</label>
                <textarea name="notes" id="notes" value={newClientData.notes} onChange={handleNewClientChange} rows={3} className="input-field" />
              </div>
              <div className="flex justify-end space-x-4">
                <button type="button" onClick={() => setShowAddClientModal(false)} className="btn-secondary">Annuler</button>
                <button type="submit" className="btn-primary">Ajouter</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default HomePage;
