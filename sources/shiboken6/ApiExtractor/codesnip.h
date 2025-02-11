// Copyright (C) 2022 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0

#ifndef CODESNIP_H
#define CODESNIP_H

#include "codesniphelpers.h"
#include "typesystem_enums.h"

#include <QtCore/QList>
#include <QtCore/QHash>
#include <QtCore/QString>

#include <variant>

QT_FORWARD_DECLARE_CLASS(QDebug)

class TemplateInstance
{
public:
    explicit TemplateInstance(QString name) : m_name(std::move(name)) {}

    void addReplaceRule(const QString &name, const QString &value)
    {
        replaceRules.insert(name, value);
    }

    QString expandCode() const;

    QString name() const
    {
        return m_name;
    }

private:
    QString m_name;
    QHash<QString, QString> replaceRules;
};

using CodeSnipFragment = std::variant<QString, TemplateInstance>;

QDebug operator<<(QDebug d, const CodeSnipFragment &codeFrag);

class CodeSnipAbstract : public CodeSnipHelpers
{
public:
    using CodeSnipFragments = QList<CodeSnipFragment>;

    QString code() const;

    void addCode(const QString &code);
    void addCode(QStringView code) { addCode(code.toString()); }

    void addTemplateInstance(const TemplateInstance &ti)
    {
        m_codeList.emplace_back(CodeSnipFragment{ti});
    }

    bool isEmpty() const { return m_codeList.empty(); }
    void purgeEmptyFragments();

    const CodeSnipFragments &codeList() const { return m_codeList; }

    static QRegularExpression placeHolderRegex(int index);

private:
    CodeSnipFragments m_codeList;
};

class TemplateEntry : public CodeSnipAbstract
{
public:
    explicit TemplateEntry(const QString &name) : m_name(name) {}

    QString name() const
    {
        return m_name;
    }

private:
    QString m_name;
};

class CodeSnip : public CodeSnipAbstract
{
public:
    CodeSnip() = default;
    explicit CodeSnip(TypeSystem::Language lang) : language(lang) {}

    TypeSystem::Language language = TypeSystem::TargetLangCode;
    TypeSystem::CodeSnipPosition position = TypeSystem::CodeSnipPositionAny;
};

/// Purge empty fragments and snippets caused by new line characters in
/// conjunction with <insert-template>.
void purgeEmptyCodeSnips(QList<CodeSnip> *list);

#endif // CODESNIP_H
