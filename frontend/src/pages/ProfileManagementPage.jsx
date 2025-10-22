import React, { useState } from 'react';
import { Edit, Key, Save, X } from 'lucide-react';
import { xbpneusClasses, xbpneusColors } from '../styles/colors';

const ProfileManagementPage = () => {
  const [editingProfile, setEditingProfile] = useState(false);
  const [editingPassword, setEditingPassword] = useState(false);
  const [profileData, setProfileData] = useState({
    name: 'João Silva',
    email: 'joao@example.com',
    phone: '(11) 98765-4321',
    company: 'Transportes Silva LTDA',
  });
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });

  const handleProfileChange = (e) => {
    const { name, value } = e.target;
    setProfileData({ ...profileData, [name]: value });
  };

  const handlePasswordChange = (e) => {
    const { name, value } = e.target;
    setPasswordData({ ...passwordData, [name]: value });
  };

  const handleSaveProfile = async () => {
    try {
      // Substituir pela chamada real à API
      // await fetch('/api/auth/me/', { method: 'PUT', body: JSON.stringify(profileData) });
      alert('Perfil atualizado com sucesso!');
      setEditingProfile(false);
    } catch (err) {
      alert('Erro ao atualizar perfil');
    }
  };

  const handleChangePassword = async () => {
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      alert('As senhas não correspondem');
      return;
    }

    try {
      // Substituir pela chamada real à API
      // await fetch('/api/auth/change-password/', { method: 'POST', body: JSON.stringify(passwordData) });
      alert('Senha alterada com sucesso!');
      setEditingPassword(false);
      setPasswordData({ currentPassword: '', newPassword: '', confirmPassword: '' });
    } catch (err) {
      alert('Erro ao alterar senha');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-2xl mx-auto">
        {/* Cabeçalho */}
        <div className="mb-8">
          <h1 className={`${xbpneusClasses.cardTitle} text-3xl mb-2`}>
            Gerenciamento de Perfil
          </h1>
          <p className="text-gray-600">Atualize suas informações pessoais e segurança</p>
        </div>

        {/* Seção de Edição de Perfil */}
        <div className={`${xbpneusClasses.card} p-6 mb-6`}>
          <div className="flex justify-between items-center mb-6">
            <h2 className={`${xbpneusClasses.cardTitle} text-xl`}>Informações Pessoais</h2>
            {!editingProfile && (
              <button
                onClick={() => setEditingProfile(true)}
                className={`${xbpneusClasses.buttonPrimary} px-4 py-2 rounded-lg flex items-center gap-2 text-sm`}
              >
                <Edit size={16} />
                Editar Perfil
              </button>
            )}
          </div>

          {editingProfile ? (
            <div className="space-y-4">
              <div>
                <label className={xbpneusClasses.inputLabel}>Nome Completo</label>
                <input
                  type="text"
                  name="name"
                  value={profileData.name}
                  onChange={handleProfileChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
              <div>
                <label className={xbpneusClasses.inputLabel}>Email</label>
                <input
                  type="email"
                  name="email"
                  value={profileData.email}
                  onChange={handleProfileChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
              <div>
                <label className={xbpneusClasses.inputLabel}>Telefone</label>
                <input
                  type="tel"
                  name="phone"
                  value={profileData.phone}
                  onChange={handleProfileChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
              <div>
                <label className={xbpneusClasses.inputLabel}>Empresa</label>
                <input
                  type="text"
                  name="company"
                  value={profileData.company}
                  onChange={handleProfileChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>

              <div className="flex gap-2 pt-4">
                <button
                  onClick={handleSaveProfile}
                  className={`${xbpneusClasses.buttonPrimary} px-6 py-2 rounded-lg flex items-center gap-2`}
                >
                  <Save size={16} />
                  Salvar Alterações
                </button>
                <button
                  onClick={() => setEditingProfile(false)}
                  className={`${xbpneusClasses.buttonSecondary} px-6 py-2 rounded-lg flex items-center gap-2`}
                >
                  <X size={16} />
                  Cancelar
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              <div>
                <p className="text-sm text-gray-600">Nome Completo</p>
                <p className={`${xbpneusClasses.cardTitle}`}>{profileData.name}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Email</p>
                <p className={`${xbpneusClasses.cardTitle}`}>{profileData.email}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Telefone</p>
                <p className={`${xbpneusClasses.cardTitle}`}>{profileData.phone}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Empresa</p>
                <p className={`${xbpneusClasses.cardTitle}`}>{profileData.company}</p>
              </div>
            </div>
          )}
        </div>

        {/* Seção de Alteração de Senha */}
        <div className={`${xbpneusClasses.card} p-6`}>
          <div className="flex justify-between items-center mb-6">
            <h2 className={`${xbpneusClasses.cardTitle} text-xl`}>Segurança</h2>
            {!editingPassword && (
              <button
                onClick={() => setEditingPassword(true)}
                className={`${xbpneusClasses.buttonPrimary} px-4 py-2 rounded-lg flex items-center gap-2 text-sm`}
              >
                <Key size={16} />
                Alterar Senha
              </button>
            )}
          </div>

          {editingPassword ? (
            <div className="space-y-4">
              <div>
                <label className={xbpneusClasses.inputLabel}>Senha Atual</label>
                <input
                  type="password"
                  name="currentPassword"
                  value={passwordData.currentPassword}
                  onChange={handlePasswordChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                  style={{ color: xbpneusColors.text.primary }}
                />
              </div>
              <div>
                <label className={xbpneusClasses.inputLabel}>Nova Senha</label>
                <input
                  type="password"
                  name="newPassword"
                  value={passwordData.newPassword}
                  onChange={handlePasswordChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                  style={{ color: xbpneusColors.text.primary }}
                />
              </div>
              <div>
                <label className={xbpneusClasses.inputLabel}>Confirmar Nova Senha</label>
                <input
                  type="password"
                  name="confirmPassword"
                  value={passwordData.confirmPassword}
                  onChange={handlePasswordChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                  style={{ color: xbpneusColors.text.primary }}
                />
              </div>

              <div className="flex gap-2 pt-4">
                <button
                  onClick={handleChangePassword}
                  className={`${xbpneusClasses.buttonPrimary} px-6 py-2 rounded-lg flex items-center gap-2`}
                >
                  <Save size={16} />
                  Alterar Senha
                </button>
                <button
                  onClick={() => setEditingPassword(false)}
                  className={`${xbpneusClasses.buttonSecondary} px-6 py-2 rounded-lg flex items-center gap-2`}
                >
                  <X size={16} />
                  Cancelar
                </button>
              </div>
            </div>
          ) : (
            <p className="text-gray-600">Clique em "Alterar Senha" para atualizar sua senha</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProfileManagementPage;

